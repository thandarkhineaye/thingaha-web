### CREATE Extrafunds
| API      | URL | Action     |
| :---        |    :----:   |          ---: |
| /api/v1/extra_funds     | Create Extra fund    | POST   |

Input Sample:
```json
{
    "mmk_amount": 30000,
    "transfer_id": 1
}
```
Output Sample:
```json
{
  "data": {
    "extra_funds": [
      {
            "id": 1,
            "mmk_amount": 100000,
            "transfer_id": {
                "id": 1,
                "year": "2020",
                "month": "january",
                "total_mmk": "35000",
                "total_jpy": "3000"
            }
       }
    ]
  }
}
```

### GET all Extrafunds
| API      | URL | Action     |
| :---        |    :----:   |          ---: |
| /api/v1/extra_funds     | GET all extra funds      | GET   |
| /api/v1/extra_funds?page=XXX     | GET all extra funds  with pagination      | GET   |

Output Sample
```json
{
    "data": {
        "count": 2,
        "extra_funds": [
            {
                "id": 1,
                "mmk_amount": 100000,
                "transfer": {
                    "id": 1,
                    "year": "2020",
                    "month": "january",
                    "total_mmk": "35000",
                    "total_jpy": "3000"
                }
            },
            {
                "id": 2,
                "mmk_amount": 200000,
                "transfer": {
                    "id": 2,
                    "year": "2020",
                    "month": "february",
                    "total_mmk": "35000",
                    "total_jpy": "3000"
                }
            }
        ],
        "new_transfers": [
            {
                "id": 4,
                "month": "march",
                "total_jpy": 200.0,
                "total_mmk": 3000.0,
                "year": 2020
            },
            {
                "id": 5,
                "month": "march",
                "total_jpy": 200.0,
                "total_mmk": 3000.0,
                "year": 2020
            }
        ]
    }
}
```

### GET Extrafund by ID
| API      | URL | Action     |
| :---        |    :----:   |          ---: |
| /api/v1/extra_funds/id     | GET extrafund by id    | GET   |

Output Sample
```json
{
  "data": {
    "extra_funds": [
      {
            "id": 2,
            "mmk_amount": 100000,
            "transfer_id": {
                "id": 2,
                "year": "2020",
                "month": "january",
                "total_mmk": "35000",
                "total_jpy": "3000"
            }
       }
    ]
  }
}
```

### UPDATE Extra fund
| API      | URL | Action     |
| :---        |    :----:   |          ---: |
| /api/v1/extra_funds/id     | update extra fund info by id     | PUT  |

Input Sample:
```json
{
    "mmk_amount": 100000,
    "transfer_id": 4
}
```

Output Sample:
```json
{
  "status": true
}
```

### DELETE Extrafund
| API      | URL | Action     |
| :---        |    :----:   |          ---: |
| /api/v1/extra_funds/id     | Delete extra fund by id     | DELETE  |

Output Sample:
```json
{
  "status": true
}
```

### ERROR 
```json
{
  "errors": {
    "error": {
      "description": "Error Description",
      "error_code": "ERROR CODE",
      "reason": "ERROR Reason"
    }
  }
}
```
- ***for error detail description please reference error.md***
