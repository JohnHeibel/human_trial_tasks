import secrets
import re
from typing import Dict, Any, Optional


class FileUploadValidator:
    """Validates uploaded files for security and generates safe storage names."""

    # Allowed file extensions (lowercase)
    ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.pdf', '.txt', '.doc', '.docx'}

    # MIME type to extension mapping
    MIME_TYPE_MAP = {
        'image/jpeg': ['.jpg', '.jpeg'],
        'image/png': ['.png'],
        'image/gif': ['.gif'],
        'application/pdf': ['.pdf'],
        'text/plain': ['.txt'],
        'application/msword': ['.doc'],
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx'],
    }

    def __init__(self, max_size_bytes: int = 10485760):
        """
        Initialize the file upload validator.

        Args:
            max_size_bytes: Maximum allowed file size in bytes (default: 10MB)
        """
        self.max_size_bytes = max_size_bytes
        self.generated_filenames = set()  # Track generated names to ensure uniqueness

    def validate_extension(self, filename: str) -> Dict[str, Any]:
        """
        Validate file extension against whitelist.

        Args:
            filename: Original filename

        Returns:
            Dictionary with 'valid' (bool) and 'message' (str)
        """
        if not filename or '.' not in filename:
            return {'valid': False, 'message': 'Filename has no extension'}

        # Get extension (everything after last dot, lowercase)
        extension = '.' + filename.rsplit('.', 1)[-1].lower()

        if extension in self.ALLOWED_EXTENSIONS:
            return {'valid': True, 'message': 'Extension allowed'}
        else:
            return {'valid': False, 'message': f'Extension {extension} not allowed'}

    def validate_mime_type(self, filename: str, mime_type: str) -> Dict[str, Any]:
        """
        Validate that MIME type matches file extension.

        Args:
            filename: Original filename
            mime_type: MIME type from file upload

        Returns:
            Dictionary with 'valid' (bool) and 'message' (str)
        """
        if not filename or '.' not in filename:
            return {'valid': False, 'message': 'Cannot validate MIME type without extension'}

        extension = '.' + filename.rsplit('.', 1)[-1].lower()

        # Check if MIME type is in our mapping
        if mime_type not in self.MIME_TYPE_MAP:
            return {'valid': False, 'message': f'MIME type {mime_type} not allowed'}

        # Check if extension matches the MIME type
        allowed_extensions = self.MIME_TYPE_MAP[mime_type]
        if extension in allowed_extensions:
            return {'valid': True, 'message': 'MIME type matches extension'}
        else:
            return {'valid': False, 'message': f'MIME type {mime_type} does not match extension {extension}'}

    def validate_file_size(self, file_size_bytes: int) -> Dict[str, Any]:
        """
        Validate file size against maximum limit.

        Args:
            file_size_bytes: Size of file in bytes

        Returns:
            Dictionary with 'valid' (bool) and 'message' (str)
        """
        if file_size_bytes < 0:
            return {'valid': False, 'message': 'Invalid file size'}

        if file_size_bytes == 0:
            return {'valid': False, 'message': 'File is empty'}

        if file_size_bytes > self.max_size_bytes:
            max_mb = self.max_size_bytes / (1024 * 1024)
            actual_mb = file_size_bytes / (1024 * 1024)
            return {'valid': False, 'message': f'File size {actual_mb:.2f}MB exceeds limit of {max_mb:.2f}MB'}

        return {'valid': True, 'message': 'File size acceptable'}

    def sanitize_filename(self, filename: str) -> str:
        """
        Sanitize filename to prevent security issues.

        Args:
            filename: Original filename to sanitize

        Returns:
            Sanitized filename safe for storage
        """
        if not filename:
            return 'unnamed'

        # Remove path components (handle both / and \)
        filename = filename.replace('\\', '/').split('/')[-1]

        # Remove null bytes
        filename = filename.replace('\0', '')

        # Split into name and extension
        if '.' in filename:
            name_part = filename.rsplit('.', 1)[0]
            extension = '.' + filename.rsplit('.', 1)[1]
        else:
            name_part = filename
            extension = ''

        # Remove dangerous characters, keep only alphanumeric, dash, underscore
        name_part = re.sub(r'[^a-zA-Z0-9_-]', '_', name_part)

        # Remove leading/trailing underscores and dashes
        name_part = name_part.strip('_-')

        # If name is empty after sanitization, use default
        if not name_part:
            name_part = 'file'

        # Limit length (keep room for extension)
        max_name_length = 250 - len(extension)
        if len(name_part) > max_name_length:
            name_part = name_part[:max_name_length]

        return name_part + extension

    def generate_unique_filename(self, original_filename: str) -> str:
        """
        Generate a unique filename for storage.

        Args:
            original_filename: Original uploaded filename

        Returns:
            Unique filename in format: {unique_id}_{sanitized_name}.{ext}
        """
        # Sanitize the original filename
        sanitized = self.sanitize_filename(original_filename)

        # Extract extension
        if '.' in sanitized:
            extension = '.' + sanitized.rsplit('.', 1)[1]
            name_without_ext = sanitized.rsplit('.', 1)[0]
        else:
            extension = ''
            name_without_ext = sanitized

        # Generate unique filename
        while True:
            unique_id = secrets.token_hex(8)  # 16 character hex string
            unique_filename = f"{unique_id}_{name_without_ext}{extension}"

            # Ensure uniqueness (very unlikely to collide, but check anyway)
            if unique_filename not in self.generated_filenames:
                self.generated_filenames.add(unique_filename)
                return unique_filename

    def validate_upload(self, filename: str, file_size_bytes: int, mime_type: str) -> Dict[str, Any]:
        """
        Perform complete validation of an uploaded file.

        Args:
            filename: Original filename
            file_size_bytes: Size of file in bytes
            mime_type: MIME type from upload

        Returns:
            Dictionary with validation results:
            {
                'valid': bool,
                'safe_filename': str or None,
                'errors': list of error messages,
                'details': dict of individual validation results
            }
        """
        errors = []
        details = {}

        # Validate extension
        ext_result = self.validate_extension(filename)
        details['extension'] = ext_result
        if not ext_result['valid']:
            errors.append(ext_result['message'])

        # Validate MIME type
        mime_result = self.validate_mime_type(filename, mime_type)
        details['mime_type'] = mime_result
        if not mime_result['valid']:
            errors.append(mime_result['message'])

        # Validate file size
        size_result = self.validate_file_size(file_size_bytes)
        details['file_size'] = size_result
        if not size_result['valid']:
            errors.append(size_result['message'])

        # Generate safe filename if all validations passed
        safe_filename = None
        if not errors:
            safe_filename = self.generate_unique_filename(filename)

        return {
            'valid': len(errors) == 0,
            'safe_filename': safe_filename,
            'errors': errors,
            'details': details
        }
