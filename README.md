# Lunch Voting Backend

A Django REST Framework API for employees to vote on daily lunch menus.

## Features
- JWT authentication
- CRUD for restaurants, menus, and employees
- Daily voting system with one vote per employee per day
- Endpoints for today’s menu and voting results

## Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/anastasia-butkevich/lunch-voting-system.git
   cd lunch-voting-system
   ````

2. Create `.env` file with environment variables:

   ```
   SECRET_KEY=your_secret_key
   DEBUG=True
   DB_NAME=lunch_db
   DB_USER=user
   DB_PASSWORD=password
   DB_HOST=db
   DB_PORT=5432
   ```
3. Start services:

   ```bash
   docker-compose up --build
   ```

## API Endpoints

| Method | Endpoint              | Description                    | Auth Required |
| ------ | --------------------- | ------------------------------ | ------------- |
| POST   | `/api/auth/login/`    | Get JWT token                  | No            |
| POST   | `/api/restaurants/`   | Create restaurant              | Yes           |
| POST   | `/api/menus/`         | Upload menu                    | Yes           |
| GET    | `/api/menus/today/`   | Get today’s menus              | Yes           |
| GET    | `/api/menus/results/` | Get voting results for today   | Yes           |
| POST   | `/api/employees/`     | Create employee with user data | Yes           |
| POST   | `/api/votes/`         | Vote for a menu                | Yes           |

## Headers

* `Authorization: Bearer <token>`
* `X-App-Build: <int>` (optional, for multi-version client support)

## Testing

```bash
docker compose exec backend pytest
```

## Linting

```bash
flake8
```