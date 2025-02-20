from sqlalchemy import Column, Integer, String, Float, Date, Integer, ForeignKey
from sqlalchemy.orm import relationship
import os

if "RENDER" in os.environ:
    from backend.database.db import Base
else:
    from database.db import Base


class Users_info(Base):
    __tablename__ = "users_info"

    id = Column(Integer, primary_key=True, index=True)
    fname = Column(String(255), index=True)
    lname = Column(String(255), index=True)
    work_email = Column(String(255), index=True)
    hashed_password = Column(String(100), nullable=False)
    email_verified = Column(String(255), index=True)
    last_login = Column(String(255), index=True)
    role = Column(String(50), default="user")  # Can be "user", "admin", "superadmin"

class Employee(Base):
    __tablename__ = "individual_clients"
    id = Column(Integer, primary_key=True, autoincrement=True)
    employee_id = Column(Integer, primary_key=True, index=True)
    lastname = Column(String(255), nullable=False)
    othernames = Column(String(255), nullable=False)
    residential_address = Column(String(255))
    postal_address = Column(String(255))
    client_phone_no = Column(String(50), nullable=False)
    title = Column(String(50))
    marital_status = Column(String(50))
    gender = Column(String(10))
    date_of_birth = Column(Date)
    employer = Column(String(255))
    previous_employee_no = Column(String(100))
    social_security_no = Column(String(100))
    voters_id_no = Column(String(100))
    employment_date = Column(Date)
    next_of_kin = Column(String(255))
    next_of_kin_contact = Column(String(50))
    next_of_kin_address = Column(String(255))
    search_name = Column(String(255), index=True)


class Security(Base):
    __tablename__ = "loan_security"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    client_fk = Column(Integer, ForeignKey('individual_clients.id'), nullable=False)
    collateral_description = Column(String(255), nullable=False)
    collateral_value = Column(Float, nullable=False)
    forced_sale_value = Column(Float, nullable=False)
    method_of_valuation = Column(String(100), nullable=False)
    cash_or_non_cash = Column(String(50), nullable=False)
    
    client = relationship("Employee", backref="securities")

class Repayment(Base):
    __tablename__ = "repayments"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    repayment_date = Column(Date, nullable=False)
    repayment_amounts = Column(Float, nullable=False)

class Guarantee(Base):
    __tablename__ = "guarantee"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    guarantor = Column(String(255), nullable=False)
    pledged_amount = Column(Float, nullable=False)

class DefaultDefinition(Base):
    __tablename__ = "default_definition"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    clients_group = Column(String(255), nullable=False)
    overdue_days_repr_default = Column(Integer, nullable=False)

class OtherLoansDisclosed(Base):
    __tablename__ = "other_loans_disclosed"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    loan_amount = Column(Float, nullable=False)
    extending_party = Column(String(255), nullable=False)

class Macros(Base):
    __tablename__ = "macros"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    employment_rate = Column(Float, nullable=False)
    inflation_rate = Column(Float, nullable=False)
    gdp = Column(Float, nullable=False)



class Loan(Base):
    __tablename__ = "loans"

    id = Column(Integer, primary_key=True, autoincrement=True)
    loan_no = Column(String(50), index=True)
    employee_id = Column(String(50), index=True)
    employee_name = Column(String(255))
    employer = Column(String(255))
    loan_issue_date = Column(Date)
    deduction_start_period = Column(String(50))
    submission_period = Column(String(50))
    maturity_period = Column(String(50))
    location_code = Column(String(50))
    dalex_paddy = Column(String(50))
    team_leader = Column(String(255))
    loan_type = Column(String(255))
    loan_amount = Column(Float)
    loan_term = Column(Integer)
    administrative_fees = Column(Float)
    total_interest = Column(Float)
    total_collectible = Column(Float)
    net_loan_amount = Column(Float)
    monthly_installment = Column(Float)
    principal_due = Column(Float)
    interest_due = Column(Float)
    total_due = Column(Float)
    principal_paid = Column(Float)
    interest_paid = Column(Float)
    total_paid = Column(Float)
    principal_paid2 = Column(Float)
    interest_paid2 = Column(Float)
    total_paid2 = Column(Float)
    paid = Column(Float)
    cancelled = Column(Float)
    outstanding_loan_balance = Column(Float)
    accumulated_arrears = Column(Float)
    ndia = Column(Float)
    prevailing_posted_repayment = Column(Float)
    prevailing_due_payment = Column(Float)
    current_missed_deduction = Column(Float)
    admin_charge = Column(Float)
    recovery_rate = Column(Float)
    deduction_status = Column(String(50))
