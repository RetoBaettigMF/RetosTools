## Table: activities
| Field | Type     |
|-------|----------|
| Id | int(11)|
| Number | int(11)|
| Name | longtext|
| StartDate | date|
| EndedDate | date|
| BudgetSeconds | bigint(20)|
| SubprojectId | int(11)|
| BillabilityId | int(11)|
| PlannedSeconds | bigint(20)|

## Table: auditlogs
| Field | Type     |
|-------|----------|
| Id | int(11)|
| UserId | char(36)|
| DateTime | datetime(2)|
| OldValues | longtext|
| NewValues | longtext|

## Table: billabilities
| Field | Type     |
|-------|----------|
| Id | int(11)|
| Name | longtext|
| IsBillable | tinyint(1)|
| SortingWeight | int(11)|
| Inactive | tinyint(1)|

## Table: editlocks
| Field | Type     |
|-------|----------|
| Id | int(11)|
| Date | date|

## Table: favouriteactivities
| Field | Type     |
|-------|----------|
| UserId | char(36)|
| ActivityId | int(11)|

## Table: recordentries
| Field | Type     |
|-------|----------|
| Id | int(11)|
| RecordId | int(11)|
| DurationSeconds | bigint(20)|
| Begin | time|
| PauseSeconds | bigint(20)|
| Comment | longtext|
| ActivityId | int(11)|

## Table: records
| Field | Type     |
|-------|----------|
| Id | int(11)|
| Date | date|
| UserId | char(36)|
| PaidLeaveType | int(11)|
| PaidLeaveReason | longtext|

## Table: subprojects
| Field | Type     |
|-------|----------|
| Id | int(11)|
| Number | int(11)|
| Name | longtext|
| ProjectNumber | int(11)|
| ProjectName | longtext|
| CustomerName | longtext|
| ManagerId | char(36)|
| DeputyManagerId | char(36)|
| ArchitectId | char(36)|

## Table: userbalancecorrections
| Field | Type     |
|-------|----------|
| Id | int(11)|
| UserId | char(36)|
| Date | date|
| OvertimeSeconds | bigint(20)|
| VacationSeconds | bigint(20)|

## Table: userparttimesettings
| Field | Type     |
|-------|----------|
| Id | int(11)|
| UserId | char(36)|
| StartDate | date|
| Factor | double|

## Table: users
| Field | Type     |
|-------|----------|
| Id | char(36)|
| GoogleId | varchar(255)|
| FirstName | longtext|
| LastName | longtext|
| Email | longtext|
| AvatarUrl | longtext|
| Role | int(11)|
| EntryDate | date|
| LeftDate | date|
| IsConfirmed | tinyint(1)|

## Table: uservacationdayssettings
| Field | Type     |
|-------|----------|
| Id | int(11)|
| UserId | char(36)|
| StartDate | date|
| VacationDaysPerYear | int(11)|
