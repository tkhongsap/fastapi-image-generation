# API Documentation Changelog

## [1.1.0] - 2025-04-27

### Fixed
- Resolved OpenAPI specification version issues by adding `openapi_version="3.0.2"`
- Fixed ReDoc rendering problems with enhanced CSS styling
- Improved iframe loading experience with loading indicators
- Enhanced Swagger UI styling to better match the application theme
- Fixed responsive design issues on smaller screens
- Added proper API tags configuration for better documentation organization

### Added
- Loading indicator for API documentation pages
- Improved test script with OpenAPI schema validation
- Enhanced active link styles in the API documentation navigation
- Better error handling for iframe loading

## [1.0.0] - 2025-04-26

### Added
- Created custom API documentation at `/api` using ReDoc
- Added interactive API testing at `/docs` using Swagger UI
- Added navigation link to API documentation in the main menu
- Created custom theming for ReDoc to match site's gradient style
- Added code samples for the `/api/v1/generate/` endpoint in three languages:
  - cURL
  - Python
  - JavaScript
- Created a test script to verify API documentation endpoints
- Added custom error handling for API documentation routes
- Created detailed API documentation implementation summary in `API_DOCUMENTATION.md`

### Changed
- Modified the main FastAPI application to use custom documentation routes
- Updated the base template to include API link in navigation
- Updated OpenAPI schema configuration to support code samples
- Changed API endpoint documentation to include more detailed descriptions

### Technical Details
- Applied custom CSS theming to match the site's dark theme and gradient style
- Used iframe embedding for both ReDoc and Swagger UI
- Added tab navigation between different API documentation formats
- Used the `openapi_extra` parameter to add code samples to endpoints 