# Project Structure

project_root/
├── main.py
├── config/
│   ├── settings.py
│   └── security.py
├── user/
│   ├── api/
│   │   └── user_routes.py
│   ├── domain/
│   │   ├── entity.py
│   │   ├── aggregate_root.py
│   │   └── value_objects.py
│   ├── infra/
│   │   ├── database.py
│   │   └── services/
│   │       └── email_client.py
│   ├── use_case/
│   │   ├── create_user_use_case.py
│   │   └── get_user_use_case.py
│   └── tests/
│       ├── test_user_routes.py
│       ├── test_create_user_use_case.py
│       └── test_get_user_use_case.py
├── order/
│   ├── api/
│   │   └── order_routes.py
│   ├── domain/
│   │   ├── entity.py
│   │   ├── aggregate_root.py
│   │   └── value_objects.py
│   ├── infra/
│   │   ├── database.py
│   │   └── services/
│   │       └── payment_gateway.py
│   ├── use_case/
│   │   ├── create_order_use_case.py
│   │   └── get_order_use_case.py
│   └── tests/
│       ├── test_order_routes.py
│       ├── test_create_order_use_case.py
│       └── test_get_order_use_case.py
