from fastapi import APIRouter, File, UploadFile, HTTPException, Depends
from sqlalchemy.orm import Session
from io import BytesIO
import pickle
import pandas as pd
import os
from database.db_models import Users_info, Employee, Loan
from database.pydantic_models import UserBase, LoanDetailsCreate, LoanDetailsResponse
from fastapi import FastAPI, File, UploadFile, HTTPException, Depends
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from security.auth import hash_password, create_access_token, verify_password, get_current_user

if "RENDER" in os.environ:
    from backend.utils.loan_functions import upload_file
    from backend.database import db_operations
    from backend.database.db import get_db

else:
    from utils.loan_functions import upload_file
    from database import db_operations
    from database.db import get_db


router = APIRouter()

@router.post("/register")
def register_user(user: UserBase, db: Session = Depends(get_db)):
    """Register a new user."""
    
    # Check if the work_email already exists
    existing_user = db.query(Users_info).filter(Users_info.work_email == user.work_email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Hash the password before storing
    hashed_password = hash_password(user.password)

    # Create new user instance
    new_user = Users_info(
        fname=user.fname,
        lname=user.lname,
        work_email=user.work_email,
        hashed_password=hashed_password,  # Store hashed password
        email_verified=user.email_verified,
        last_login=user.last_login
    )

    # Add user to database
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User registered successfully", "user_id": new_user.id}


@router.post("/login")
def login_user(work_email: str, password: str, db: Session = Depends(get_db)):
    """Authenticate user and return JWT token."""
    
    # Find user in the database
    user = db.query(Users_info).filter(Users_info.work_email == work_email).first()
    
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    # Generate JWT token
    token_data = {"sub": user.work_email, "role": user.role}
    access_token = create_access_token(token_data)
    
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/test_me")
def protected_route(user: dict = Depends(get_current_user)):
    """A protected route that requires authentication."""
    return {"message": f"Welcome, {user['sub']}!"}

@router.post("/upload-employees/")
async def upload_employees(file: UploadFile = File(...), db: Session = Depends(get_db)):
    # Read the file
    contents = await file.read()
    file_extension = file.filename.split(".")[-1].lower()
    
    try:
        if file_extension == "csv":
            df = pd.read_csv(BytesIO(contents))
        elif file_extension in ["xls", "xlsx"]:
            df = pd.read_excel(BytesIO(contents))
        else:
            raise HTTPException(status_code=400, detail="Unsupported file format. Use CSV or Excel.")
        
        # Process and insert into database
        for _, row in df.iterrows():
            employee = Employee(
                employee_id=row["Employee Id"],
                lastname=row["Lastname"],
                othernames=row["Othernames"],
                residential_address=row["Residential Address"],
                postal_address=row["Postal Address"],
                client_phone_no=row["Client Phone No."],
                title=row["Title"],
                marital_status=row["Marital Status"],
                gender=row["Gender"],
                date_of_birth=row["Date of Birth"],
                employer=row["Employer"],
                previous_employee_no=row["Previous Employee No."],
                social_security_no=row["Social Security No."],
                voters_id_no=row["Voters Id No."],
                employment_date=row["Employment Date"],
                next_of_kin=row["Next of Kin"],
                next_of_kin_contact=row["Next of Kin Contact:"],
                next_of_kin_address=row["Next of Kin Address"],
                search_name=row["Search Name"]
            )
            db.add(employee)

        db.commit()
        return {"message": "Employees uploaded successfully"}
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/upload-loans/")
async def upload_loans(file: UploadFile = File(...), db: Session = Depends(get_db)):
    # Ensure file is Excel or CSV
    if not file.filename.endswith((".xlsx", ".xls", ".csv")):
        raise HTTPException(status_code=400, detail="Invalid file format. Upload an Excel or CSV file.")

    # Read the uploaded file into a pandas DataFrame
    try:
        if file.filename.endswith((".xlsx", ".xls")):
            df = pd.read_excel(BytesIO(await file.read()))  # Read Excel file
        else:
            df = pd.read_csv(BytesIO(await file.read()))  # Read CSV file
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading file: {str(e)}")

    # Convert DataFrame rows into Loan objects
    loans = []
    for _, row in df.iterrows():
        try:
            loan = Loan(
                loan_no=row["Loan No."],
                employee_id=row["Employee Id"],
                employee_name=row["Employee Name"],
                employer=row["Employer"],
                loan_issue_date=pd.to_datetime(row["Loan Issue Date"]),  # Convert to datetime
                deduction_start_period=row["Deduction Start Period"],
                submission_period=row["Submission Period"],
                maturity_period=row["Maturity Period"],
                location_code=row["Location Code"],
                dalex_paddy=row["Dalex Paddy"],
                team_leader=row["Team Leader"],
                loan_type=row["Loan Type"],
                loan_amount=float(row["Loan Amount"]),
                loan_term=int(row["Loan Term"]),
                administrative_fees=float(row["Administrative Fees"]),
                total_interest=float(row["Total Interest"]),
                total_collectible=float(row["Total Collectible"]),
                net_loan_amount=float(row["Net Loan Amount"]),
                monthly_installment=float(row["Monthly Installment"]),
                principal_due=float(row["Principal Due"]),
                interest_due=float(row["Interest Due"]),
                total_due=float(row["Total Due"]),
                principal_paid=float(row["Principal Paid"]),
                interest_paid=float(row["Interest Paid"]),
                total_paid=float(row["Total Paid"]),
                principal_paid2=float(row["Principal Paid2"]),
                interest_paid2=float(row["Interest Paid2"]),
                total_paid2=float(row["Total Paid2"]),
                paid=row["Paid"],
                cancelled=row["Cancelled"],
                outstanding_loan_balance=float(row["Outstanding Loan Balance"]),
                accumulated_arrears=float(row["Accumulated Arrears"]),
                ndia=row["NDIA"],
                prevailing_posted_repayment=float(row["Prevailing Posted Repayment"]),
                prevailing_due_payment=float(row["Prevailing Due Payment"]),
                current_missed_deduction=float(row["Current Missed Deduction"]),
                admin_charge=float(row["Admin Charge"]),
                recovery_rate=float(row["Recovery Rate"]),
                deduction_status=row["Deduction Status"]
            )
            loans.append(loan)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error processing row: {str(e)}")

    # Bulk insert into database
    db.add_all(loans)
    db.commit()

    return {"message": "Loans uploaded successfully", "total_records": len(loans)}





# @router.post("/predict")
# def predict_probability(input_data: dict):
#     df = pd.DataFrame([input_data])
#     probability = model.predict_proba(df)[:, 1]
#     return {"probability_of_default": probability[0]}

# @router.post("/loans/", response_model=LoanDetailsResponse)
# def create_loan(loan: LoanDetailsCreate, db: Session = Depends(get_db)):
#     db_loan = LoanDetails(**loan.dict())  # Convert Pydantic model to SQLAlchemy model
#     db.add(db_loan)
#     db.commit()
#     db.refresh(db_loan)
#     return db_loan  # SQLAlchemy model auto-converts to Pydantic

# @router.get("/loans/{loan_id}", response_model=LoanDetailsResponse)
# def get_loan(loan_id: int, db: Session = Depends(get_db)):
#     loan = db.query(LoanDetails).filter(LoanDetails.id == loan_id).first()
#     if not loan:
#         raise HTTPException(status_code=404, detail="Loan not found")
#     return loan  # FastAPI converts it to LoanDetailsResponse

































































