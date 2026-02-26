# Circle Roles & Permissions

This document outlines the role-based access control (RBAC) structure for circles in the application.

## Overview
The application uses **circle-specific roles only**. There are no global roles - all users are equal at the system level. Permissions are granted based on a user's role within each circle.

## Circle Roles

These roles apply only within a specific Circle and determine what a user can do in that circle.

| Role | Badge | Description | Permissions |
| :---: | :---: | :--- | :--- |
| **Owner** | 👑 | The creator of the Circle | • Full control over circle settings<br>• Delete the circle<br>• Change circle name and description<br>• Assign/remove moderators<br>• Remove any member<br>• All moderator permissions |
| **Moderator** | 🛡️ | Appointed by the Owner | • Delete any post in the circle<br>• Remove members from the circle<br>• Approve join requests<br>• All member permissions |
| **Member** | 👤 | Standard participant | • View posts in the circle<br>• Create new posts<br>• Comment on posts<br>• Like posts |

## Hierarchy Diagram

```mermaid
graph TD
    subgraph "Circle Roles"
        Owner[👑 Owner] -->|Appoints| Mod[🛡️ Moderator]
        Mod -->|Moderates| Mem[👤 Member]
        
        Owner -->|Can| O1[Delete circle]
        Owner -->|Can| O2[Change settings]
        Owner -->|Can| O3[Assign roles]
        
        Mod -->|Can| M1[Delete any post]
        Mod -->|Can| M2[Remove members]
        
        Mem -->|Can| Me1[View posts]
        Mem -->|Can| Me2[Create posts]
        Mem -->|Can| Me3[Comment & Like]
    end

    Permission Matrix
Action	👑 Owner	🛡️ Moderator	👤 Member
View circle posts	✅	✅	✅
Create post in circle	✅	✅	✅
Comment on posts	✅	✅	✅
Like posts	✅	✅	✅
Delete own post	✅	✅	✅
Delete any post	✅	✅	❌
Remove members	✅	✅	❌
Approve join requests	✅	✅	❌
Assign moderators	✅	❌	❌
Change circle settings	✅	❌	❌
Delete circle	✅	❌	❌
User Role Examples
A user can have different roles in different circles:

User	Circle	Role	Badge
alice	Book Club	Owner	👑
alice	Gaming	Member	👤
bob	Book Club	Moderator	🛡️
bob	Gaming	Owner	👑
charlie	Book Club	Member	👤
Key Points
No global roles - All users are equal at the system level

Roles are circle-specific - A user's permissions depend on which circle they're in

One user, multiple roles - A user can be Owner in one circle and Member in another

Badges indicate role - 👑 Owner, 🛡️ Moderator, 👤 Member (as requested by frontend)

Implementation
The roles are implemented in the database:

circle_members table has a role column with values: owner, moderator, member

No roles table - roles are defined in code as an Enum

Permissions are enforced at the API level based on the user's role in each circle