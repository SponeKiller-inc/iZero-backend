# 03 – Domain Model

## Bounded contexts

| Context | Directory | Main concepts |
|---------|-----------|---------------|
| Users | `app/domain/users` | User, UserRole, UserModule |
| Auth | `app/domain/auth` | Role, RolePermission, PermissionCode |
| Session | `app/domain/session` | Session, SessionLog, RefreshToken |
| Modules | `app/domain/modules` | Module, ModuleGroup |
| Customers | `app/domain/customers` | Customer |
| Persons | `app/domain/persons` | Person, NaturalPerson, Entrepreneur, Company |
| Addresses | `app/domain/addresses` | Address, AddressType |
| Bank | `app/domain/bank` | Bank, BankAccount |
| Shared | `app/domain/shared` | ValidityPeriod, Title (academic title catalogue), identification (RegistrationNumber, VatNumber) and contact (Phone, Email) value objects |

Entities and value objects live under `entities/` and `value_objects/` in each context; domain rules are enforced inside the entities themselves rather than documented separately here.
