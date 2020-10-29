# Structured Content Plan

## YAML File Format
### Value: enrollmentType
This setting sets the event for a single individual or a team of people
**Options:**
1. individual
2. team
#### Example:
    enrollmentType: 'individual'

### Value: publishStatus
This setting sets the content plan development stage
**Options:**
1. final
2. in review
3. draft
4. archived

#### Example:
    publishStatus: 'final'

publisher: 'SimSpace'
owner: 'b66cc204-6054-4936-a903-20be182c55c6'
name:  'Introduction to Binary and Hex'
objective: []
url:  ''
selfEnrollEnabled: True
tool:  ''
randomizeQuestions: True
resources:  []
leaderboardEnabled: False
contentModules:
  - "Introduction to Binary and Hex"
difficulty:  'beginner'
description:  "An introduction to binary and hexadecimal numbering, including how and why the values are used in computing.

Introduction to Binary and Hex
- Binary and why it is used in computing
- Binary logic operations
- Hexadecimal and why it is used in computing
Introduction to PowerShell
- PowerShell in Context
- Common Use Cases
- Basic PowerShell Scripting
- PowerShell Debugging"
eventTimeLimitMinutes: 120
workRoles: ['Vulnerability Assessment Analyst', 'Cyber Crime Investigator', 'Cyber Defense Forensics Analyst', 'Cyber Defense Incident Responder', 'Cyber Defense Analyst', 'Vulnerability Analyst']
eventRoles: ['Defensive (Blue) Team']
contentClass: {'tag': 'training', 'contents': {'tag': 'lab'}}
platformRoles: []
topics: ['PowerShell']