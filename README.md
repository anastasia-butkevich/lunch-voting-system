# Lunch Voting Backend

## Setup
1. Clone repo
2. Create `.env` file for environment variables (DB, SECRET_KEY, etc.)
3. Run Docker:
    docker-compose up --build

## API
- POST `/api/auth/login/` - get JWT token
- POST `/api/restaurants/` - create restaurant
- POST `/api/menus/` - upload menu
- GET `/api/menus/today/` - get today's menus
- GET `/api/menus/results/` - get voting results for today
- POST `/api/employees/` - create employee (with user data)
- POST `/api/votes/` - vote for menu

## Headers
- `Authorization: Bearer <token>`
- `X-App-Build: <int>` (optional, to support multiple app versions)

## Testing
- Run `pytest`

## Linting
- Run `flake8`
