# ArtGen FastAPI Service - API Documentation

This document describes the REST API endpoints provided by the ArtGen service for programmatic access.

## Base URL

All API endpoints are prefixed with `/api/v1/`.

## Authentication

Currently, authentication is optional and configured via environment variables. When enabled, you must provide an API key in the `Authorization` header:

```
Authorization: Bearer YOUR_API_KEY
```

## Endpoints

### Generate Image

Create an image from a text prompt.

**Endpoint:** `POST /api/v1/generate`

**Request Body:**

```json
{
  "prompt": "A beautiful mountain landscape at sunset",
  "model": "gpt-image-1",
  "n": 1,
  "size": "1024x1024",
  "quality": "standard",
  "format": "png",
  "background": "auto"
}
```

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `prompt` | string | Yes | The text description of the desired image |
| `model` | string | No | The AI model to use. Options: `gpt-image-1`, `dall-e-3`, `dall-e-2`. Default: `gpt-image-1` |
| `n` | integer | No | Number of images to generate (1-10). Default: `1` |
| `size` | string | No | Size of the generated image. Options: `256x256`, `512x512`, `1024x1024`, `1792x1024`, `1024x1792`. Default: `1024x1024` |
| `quality` | string | No | Quality of the generated image. Options: `standard`, `hd`. Default: `standard` |
| `format` | string | No | Format of the generated image. Options: `png`, `webp`. Default: `png` |
| `background` | string | No | Background setting. Options: `auto`, `transparent`, or a hex color code like `#FF5733`. Default: `auto` |

**Response:**

```json
{
  "created": 1745575400,
  "model": "gpt-image-1",
  "images": [
    {
      "b64_json": "<base64-encoded-image-data>",
      "filetype": "png",
      "size": "1024x1024"
    }
  ]
}
```

### Edit Image

Edit an existing image according to a text prompt.

**Endpoint:** `POST /api/v1/edit`

**Request Format:** `multipart/form-data`

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `prompt` | string | Yes | The text description of the desired edit |
| `image` | file | Yes | The image file to edit |
| `mask` | file | No | Optional mask file with transparent areas indicating where to edit |
| `model` | string | No | The AI model to use (currently only `dall-e-2` is supported) |
| `n` | integer | No | Number of edits to generate (1-10). Default: `1` |
| `size` | string | No | Size of the edited image. Options: `256x256`, `512x512`, `1024x1024`. Default: `1024x1024` |
| `format` | string | No | Format of the edited image. Options: `png`, `webp`. Default: `png` |

**Response:** Same format as the Generate Image endpoint.

### Create Variation

Create variations of an existing image.

**Endpoint:** `POST /api/v1/variation`

**Request Format:** `multipart/form-data`

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `image` | file | Yes | The image file to create variations of |
| `model` | string | No | The AI model to use (currently only `dall-e-2` is supported) |
| `n` | integer | No | Number of variations to generate (1-10). Default: `1` |
| `size` | string | No | Size of the variation images. Options: `256x256`, `512x512`, `1024x1024`. Default: `1024x1024` |
| `format` | string | No | Format of the variation images. Options: `png`, `webp`. Default: `png` |

**Response:** Same format as the Generate Image endpoint.

## Error Handling

All errors are returned with an appropriate HTTP status code and a JSON response body:

```json
{
  "error": true,
  "message": "Error message describing what went wrong",
  "details": {
    "field_name": "Specific error for this field"
  }
}
```

Common error status codes:

- `400 Bad Request`: Invalid parameters or input
- `401 Unauthorized`: Missing or invalid API key
- `429 Too Many Requests`: Rate limit exceeded
- `500 Internal Server Error`: Server-side error

## Code Examples

### Python

```python
import requests
import json
import base64

# Generate an image
url = "http://localhost:8000/api/v1/generate"
payload = {
    "prompt": "A futuristic city skyline at night with flying cars",
    "model": "gpt-image-1",
    "n": 1,
    "size": "1024x1024",
    "quality": "standard",
    "format": "png"
}
headers = {
    "Content-Type": "application/json"
}

response = requests.post(url, headers=headers, json=payload)
data = response.json()

# Save the first image
if response.status_code == 200 and data["images"]:
    image_data = base64.b64decode(data["images"][0]["b64_json"])
    with open("generated_image.png", "wb") as f:
        f.write(image_data)
    print("Image saved as generated_image.png")
else:
    print(f"Error: {response.status_code}")
    print(response.text)
```

### JavaScript/Node.js

```javascript
const axios = require('axios');
const fs = require('fs');

// Generate an image
async function generateImage() {
  try {
    const response = await axios.post('http://localhost:8000/api/v1/generate', {
      prompt: 'A beautiful sunset over mountains',
      model: 'gpt-image-1',
      n: 1,
      size: '1024x1024',
      quality: 'standard',
      format: 'png'
    }, {
      headers: {
        'Content-Type': 'application/json'
      }
    });
    
    // Save the first image
    if (response.data.images && response.data.images.length > 0) {
      const imageData = Buffer.from(response.data.images[0].b64_json, 'base64');
      fs.writeFileSync('generated_image.png', imageData);
      console.log('Image saved as generated_image.png');
    }
  } catch (error) {
    console.error('Error:', error.response ? error.response.data : error.message);
  }
}

generateImage();
```

### cURL

```bash
curl -X POST "http://localhost:8000/api/v1/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "A beautiful mountain landscape at sunset",
    "model": "gpt-image-1",
    "n": 1,
    "size": "1024x1024",
    "quality": "standard",
    "format": "png"
  }' \
  -o response.json
``` 