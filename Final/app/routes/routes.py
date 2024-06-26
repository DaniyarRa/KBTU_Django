from datetime import datetime
from pytz import timezone
from fastapi import APIRouter, Depends, HTTPException, Request, Form
from fastapi.responses import JSONResponse, HTMLResponse, Response
from psycopg2.extras import Json
from sqlalchemy.orm import Session
from app.utils.tokens import create_token, revoked_tokens, verify_token
from app.db.session import get_db
from app.utils.utils import get_century_and_gender
from app.models.models import Authorization, User, Application, ProfileUpdateApplication, Session
from worker.tasks import create_application, change_status
from sqlalchemy import desc

router = APIRouter()

@router.post("/register")
async def register(request: Request, db: Session = Depends(get_db)):
    try:
        data = await request.json()
        iinbin = data.get("iinbin")
        year = int(iinbin[:2])
        month = iinbin[2:4]
        day = iinbin[4:6]
        century_and_gender_num = int(iinbin[6])
        century_and_gender = get_century_and_gender(century_and_gender_num)
        year = year + century_and_gender["century"]
        gender = century_and_gender["gender"]
        birthdate = f"{year}-{month}-{day}"
        password = data.get("password")
        fullname = data.get("name")
        birthplace = data.get("birthplace")
        nation = data.get("nation")

        new_authorization = Authorization(
            iinbin=iinbin,
            password=password
        )

        db.add(new_authorization)
        db.commit()

        new_user = User(
            id=new_authorization.id,
            fullname=fullname,
            birthdate=birthdate,
            birthplace=birthplace,
            nation=nation,
            gender=gender
        )

        db.add(new_user)
        db.commit()

        return {"message": "Account created successfully"}
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=401)
    finally:
        try:
            db.close()
        except:
            print('Connection already closed')


@router.post("/login")
async def login(request: Request, db: Session = Depends(get_db)):
    try:
        data = await request.json()
        iinbin = data.get("iinbin")
        password = data.get("password")

        auth = db.query(Authorization).filter(Authorization.iinbin == iinbin).first()
        auth_id = str(auth.id)
        if not auth:
            raise HTTPException(status_code=404, detail="User not found")

        if not auth.verify_password(password):
            raise HTTPException(status_code=401, detail="Incorrect password")

        role = "manager" if auth.is_manager else "client"

        token_data = {"sub": auth_id}
        access_token = create_token(token_data)
        if auth_id in revoked_tokens:
            revoked_tokens.discard(auth_id)
        response_data = {"access_token": access_token, "token_type": "bearer", "role": role}

        new_session = Session(
            auth_id=auth.id
        )
        db.add(new_session)
        db.commit()

        return JSONResponse(content=response_data, status_code=200)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=401)
    finally:
        try:
            db.close()
        except:
            print('Connection already closed')


@router.post("/logout")
async def logout(token: str = Depends(verify_token), db: Session = Depends(get_db)):
    try:
        revoked_tokens.add(token["sub"])
        session = db.query(Session).filter(Session.auth_id == token["sub"]).order_by(desc(Session.session_started_at)).first()

        if session:
            session.session_finished_at = datetime.now()
            db.commit()

        return Response(status_code=200)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=401)
    finally:
        try:
            db.close()
        except:
            print('Connection already closed')


@router.get("/profile", response_model=dict)
async def profile(token: str = Depends(verify_token), db: Session = Depends(get_db)):
    try:
        user_id = token["sub"]

        user = db.query(User).filter(User.id == user_id).first()
        user_data = {
            'iinbin': user.auth.iinbin,
            'fullname': user.fullname,
            'birthdate': user.birthdate,
            'birthplace': user.birthplace,
            'nation': user.nation,
            'gender': user.gender,
            'email': user.email,
            'phone_number': user.phone_number,
            'address': user.address
        }
        user_data = {key: 'Нет Данных' if value is None or value == "" else value for key, value in
                     user_data.items()}
        return user_data
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=401)
    finally:
        try:
            db.close()
        except:
            print('Connection already closed')


@router.post("/update_profile")
async def update_profile(request: Request, token: str = Depends(verify_token)):
    try:
        data = await request.json()
        user_id = token["sub"]

        create_application.delay(user_id, data)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=401)


@router.get("/applications")
async def get_applications(token: str = Depends(verify_token), db: Session = Depends(get_db)):
    try:
        user_id = token["sub"]
        auth = db.query(Authorization).filter(Authorization.id == user_id).first()

        if auth.is_manager:
            all_applications = (db.query(Application).filter(Application.status_id == 2).all())

            all_applications = [{'id': app.id,
                                 'iinbin': app.user.auth.iinbin,
                                 'created_at': app.created_at}
                                for app in all_applications]

            return {'data': all_applications}
        else:
            user = db.query(User).filter(User.id == user_id).first()
            user_applications = user.user_applications

            if not user_applications:
                raise HTTPException(status_code=401, detail="Profile not found")

            user_applications = [{'id': app.id,
                                  'created_at': app.created_at,
                                  'updated_at': app.updated_at,
                                  'closed_at': app.closed_at,
                                  'status': app.status.name}
                                 for app in user_applications]

            return {'data': user_applications}
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=401)
    finally:
        try:
            db.close()
        except:
            print('Connection already closed')


@router.post("/application_detail")
async def get_application_detail(request: Request, token: str = Depends(verify_token), db: Session = Depends(get_db)):
    try:
        data = await request.json()
        application_id = data.get("id_app")

        application_detail = db.query(ProfileUpdateApplication).filter(ProfileUpdateApplication.application_id == application_id)
        application_detail = [{'column': row.key,
                              'old_value': row.old_value or 'Нет Данных',
                              'new_value': row.new_value}
                             for row in application_detail]

        return {'data': application_detail}
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=401)
    finally:
        try:
            db.close()
        except:
            print('Connection already closed')


@router.post("/update_application_status")
async def update_application_status(request: Request, token: str = Depends(verify_token)):
    try:
        data = await request.json()
        manager_id = token["sub"]
        application_id = data.get("id_app")
        is_approved = data.get("is_approved")

        change_status.delay(manager_id, application_id, is_approved)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=401)

@router.post("/confirm_application")
async def confirm_application(application_id: str = Form(...), db: Session = Depends(get_db)):
    try:
        application = db.query(Application).filter(Application.status_id == 1, Application.id == application_id,
                                                   Application.expires_at > datetime.now(timezone('UTC')).astimezone(timezone('Asia/Almaty'))).first()

        if application:
            application.status_id = 2

            db.commit()
            return HTMLResponse(content='<html><body><h2>Application confirmed successfully.</h2></body></html>')
        else:
            return HTMLResponse(content='<html><body><h2>You have already confirmed or time was expired.</h2></body></html>')
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=401)
    finally:
        try:
            db.close()
        except:
            print('Connection already closed')

