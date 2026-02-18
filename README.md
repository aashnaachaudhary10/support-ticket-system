# Support Ticket System with AI Integration



## Overview
A modern full-stack Support Ticket System built with **React**, **Django REST Framework**, and **PostgreSQL**. The system integrates an **AI (LLM)** to automatically suggest ticket **category** and **priority** based on the ticket description. Users can review and override these suggestions before submission.  

This project demonstrates **full-stack development skills**, **LLM integration**, and **containerized deployment using Docker**.  

---

## Tech Stack

- **Frontend:** React  
- **Backend:** Django + Django REST Framework  
- **Database:** PostgreSQL  
- **LLM Integration:** OpenAI GPT-4 API  
- **Deployment:** Docker + Docker Compose  
- **Styling:** Modern CSS (card layout, responsive grid, clean UI)  

---

## Features

- Submit tickets with **title, description, category, and priority**  
- AI-powered **category & priority suggestions**  
- Browse tickets with **filters & search**  
- Update ticket status (**open → in_progress → resolved → closed**)  
- **Statistics dashboard**: total tickets, open tickets, average per day, priority & category breakdowns  
- Fully containerized for **easy deployment**  

---



## Demo

You can run this project locally using **Docker Compose**.

---

## Setup Instructions

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd SupportTicketSystem
Set your LLM API key (OpenAI GPT-4)

export LLM_API_KEY="your_api_key_here"
Run the project using Docker Compose

docker-compose up --build
Access the application

Frontend: http://localhost:3000

Backend API: http://localhost:8000/api

API Endpoints
Method	Endpoint	Description
POST	/api/tickets/	Create a new ticket
GET	/api/tickets/	List all tickets (with filters/search)
PATCH	/api/tickets/<id>/	Update ticket status/category/priority
GET	/api/tickets/stats/	Aggregated statistics (DB-level)
POST	/api/tickets/classify/	Suggest category & priority using AI
LLM Used & Why
OpenAI GPT-4 API used to automatically suggest ticket category and priority.

Chosen for accuracy, speed, and ease of integration with Python.

Example:
User enters: "I cannot login to my account"
LLM suggests:

{
  "suggested_category": "account",
  "suggested_priority": "high"
}
Design Decisions
Frontend: React functional components, modern card layout, CSS grid for stats

Backend: Django REST Framework, clean API endpoints

Database: PostgreSQL with constraints at DB level

Stats endpoint: Aggregation at database level using Django ORM

Dockerized: Backend, frontend, PostgreSQL

Error Handling: AI classify fails → tickets can still be submitted

Future Improvements
Add filter dropdowns for tickets (category/priority/status)

Truncate long descriptions with “Read more”

Mobile responsiveness improvements

Add real-time notifications when ticket status changes

Author
Aashna Chaudhary
B.Tech CSE (AIML) | Aspiring Full Stack Developer
LinkedIn | Portfolio
