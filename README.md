
python -m venv eventenv
source eventenv/bin/activate
pip install -r requirements.txt

python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver

### Apps

- `accounts` — custom user model, auth (register/login/logout), vendor profiles
- `events` — event CRUD, browse/search/filter
- `bookings` — ticket booking with seat-locking to prevent overselling
- `referrals` — referral network (referral code + `referred_by`)
- `dashboard` — custom staff dashboard (no Django admin)
 
### API Endpoints

### Auth
| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/auth/register/` | Register (optional referral code) |
| POST | `/api/auth/login/` | Login, returns token |
| POST | `/api/auth/logout/` | Logout |
| GET | `/api/auth/me/` | Current user profile |

### Events
| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/events/` | Browse/search/filter events |
| GET | `/api/events/{id}/` | Event detail |
| POST | `/api/events/` | Create event (staff only) |
| PATCH | `/api/events/{id}/` | Update event (staff only) |

### Bookings
| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/bookings/` | Book tickets |
| GET | `/api/bookings/` | Booking history |
| POST | `/api/bookings/{id}/cancel/` | Cancel booking |

### Referrals
| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/referrals/{user_id}/tree/` | Referral tree |
| GET | `/api/referrals/{user_id}/root/` | Root referrer |
| GET | `/api/referrals/{user_id}/stats/` | Referral stats |
