# 🚀 Leave Management System — Web App with .NET Integration

A full-stack **Leave Management System** built using **Flask + MS SQL Server**, with a complementary **.NET Core MVC reporting module** for HR analytics. This project demonstrates enterprise-style integration between **Python (Flask)** and **.NET Core MVC** using a shared database architecture.

---

## 🧰 Tech Stack

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![MS SQL Server](https://img.shields.io/badge/MS_SQL_Server-CC2927?style=for-the-badge&logo=microsoftsqlserver&logoColor=white)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)
![.NET](https://img.shields.io/badge/.NET_Core_MVC-512BD4?style=for-the-badge&logo=dotnet&logoColor=white)
![Git](https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white)
![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white)

---

## 📌 Overview

The Leave Management System automates employee leave workflows:

- Employees apply for leave
- Managers approve/reject requests
- HR views reports via .NET MVC module
- All modules use a shared **MS SQL Server database**

---

## ✨ Features

### 👨‍💼 Employee
- Login (session-based)
- Apply for leave
- View status
- Check leave balance

### 🧑‍💻 Manager
- Approve / reject leave requests
- View team requests

### 🏢 HR (.NET MVC)
- Leave summary reports
- Employee-wise analytics
- Read-only dashboard

---

## 🏗️ Architecture

Flask App → MS SQL Server → .NET MVC Reporting Module

- Flask handles business logic
- SQL Server stores all data
- Stored procedures manage approvals & balance updates
- .NET MVC provides reporting layer

---

## ⚙️ Setup

```bash
git clone https://github.com/AkshitOG/Leave-Management-System.git
cd Leave-Management-System
pip install -r requirements.txt
python app.py