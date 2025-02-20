from pydantic import BaseModel, EmailStr, Field
from datetime import date
from typing import Optional

# ================== Pydantic Models ==================

class UserBase(BaseModel):
    fname: str
    lname: str
    work_email: EmailStr
    password: str
    email_verified: str
    last_login: Optional[str] = None

class UserResponse(UserBase):
    id: int
    class Config:
        from_attributes = True

class UserLogin(UserBase):
    username: str
    password: str

class LoanDetailsBase(BaseModel):
    principal: float = Field(..., gt=0)
    annual_interest_rate: float = Field(..., gt=0)
    term_years: int = Field(..., gt=0)
    payment_frequency: str = Field(..., pattern="^(monthly|quarterly|yearly)$")
    start_date: date

class LoanDetailsCreate(LoanDetailsBase):
    pass  # Used for creating a new loan
    
class LoanDetailsResponse(LoanDetailsBase):
    id: int
    class Config:
        from_attributes = True

class ClientBase(BaseModel):
    type: str
    fname: str
    middlename: Optional[str] = None
    lastname: str
    physical_address: Optional[str] = None
    others: Optional[str] = None
    age: int = Field(..., gt=0)
    employment_type: str
    employment_history: Optional[str] = None
    repayment_approach: str

class ClientResponse(ClientBase):
    id: int
    class Config:
        from_attributes = True

class SecurityBase(BaseModel):
    client_fk: int = Field(..., gt=0)
    collateral_description: str
    collateral_value: float = Field(..., gt=0)
    forced_sale_value: float = Field(..., gt=0)
    method_of_valuation: str
    cash_or_non_cash: str

class SecurityResponse(SecurityBase):
    id: int
    class Config:
        from_attributes = True

class RepaymentBase(BaseModel):
    repayment_date: date
    repayment_amounts: float = Field(..., gt=0)

class RepaymentResponse(RepaymentBase):
    id: int
    class Config:
        from_attributes = True

class GuaranteeBase(BaseModel):
    guarantor: str
    pledged_amount: float = Field(..., gt=0)

class GuaranteeResponse(GuaranteeBase):
    id: int
    class Config:
        from_attributes = True

class DefaultDefinitionBase(BaseModel):
    clients_group: str
    overdue_days_repr_default: int = Field(..., gt=0)

class DefaultDefinitionResponse(DefaultDefinitionBase):
    id: int
    class Config:
        from_attributes = True

class OtherLoansDisclosedBase(BaseModel):
    loan_amount: float = Field(..., gt=0)
    extending_party: str

class OtherLoansDisclosedResponse(OtherLoansDisclosedBase):
    id: int
    class Config:
        from_attributes = True

class MacroEcosBase(BaseModel):
    employment_rate: float = Field(..., ge=0, le=100)
    inflation_rate: float
    gdp: float

class MacroEcosResponse(MacroEcosBase):
    id: int
    class Config:
        from_attributes = True
