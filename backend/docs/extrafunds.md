### CREATE Extrafunds
| API      | URL | Action     |
| :---        |    :----:   |          ---: |
| /api/v1/extrafunds     | Create Extrafund    | POST   |

Input Sample:
```json
{
    "mmk_amount": "30000",
    "transfer_id": "1"
}
```
Output Sample:
```json
{
    "data": {
        "extrafund": {
<<<<<<< Updated upstream
            "mmk_amount": "30000",
=======
            "mmk_amount": "10000",
>>>>>>> Stashed changes
            "transfer_id": "1"
        }
    }
}
```

### GET all Extrafunds
| API      | URL | Action     |
| :---        |    :----:   |          ---: |
| /api/v1/extrafunds     | GET all extrafunds      | GET   |

Output Sample
```json
{
    "data": {
        "count": 2,
        "extrafunds": [
            {
<<<<<<< Updated upstream
                "mmk_amount": "30000",
                "transfer_id": "1"
            },
            {
                "mmk_amount": "40000",
=======
                "mmk_amount": "10000",
                "transfer_id": "1"
            },
            {
                "mmk_amount": "30000",
>>>>>>> Stashed changes
                "transfer_id": "2"
            }
        ]
    }
}
```

### GET Extrafund by ID
| API      | URL | Action     |
| :---        |    :----:   |          ---: |
| /api/v1/extrafunds/id     | GET extrafund by id    | GET   |

Output Sample
```json
{
    "data": {
        "extrafund": {
            "mmk_amount": "30000",
<<<<<<< Updated upstream
            "transfer_id": "1"
=======
            "transfer_id": "2"
>>>>>>> Stashed changes
        }
    }
}
```

### UPDATE Extrafund
| API      | URL | Action     |
| :---        |    :----:   |          ---: |
| /api/v1/extrafunds/id     | update extrafund info by id     | PUT  |

Input Sample:
```json
{
<<<<<<< Updated upstream
    "mmk_amount": "30000",
=======
    "mmk_amount": "50000",
>>>>>>> Stashed changes
    "transfer_id": "1"
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
| /api/v1/extrafunds/id     | Delete extrafund by id     | DELETE  |

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
