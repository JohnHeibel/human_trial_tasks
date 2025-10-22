# Task 7: File Upload Validator

## Task Description

Implement a secure file upload validation system that checks uploaded files for safety before storing them. This is a critical security component that prevents malicious file uploads, path traversal attacks, and storage issues.

**Core Functionality:**
- Validate file extensions against a whitelist
- Check MIME types match expected extensions
- Enforce file size limits
- Generate safe, unique filenames for storage
- Sanitize filenames to prevent path traversal and other attacks
- Provide detailed validation results

**Requirements:**

1. **Extension Validation**: Check file extensions against a whitelist
   - Allowed extensions: `.jpg`, `.jpeg`, `.png`, `.gif`, `.pdf`, `.txt`, `.doc`, `.docx`
   - Case-insensitive extension checking
   - Reject files with dangerous extensions (`.exe`, `.sh`, `.bat`, `.php`, etc.)

2. **MIME Type Validation**: Verify MIME types match file extensions
   - Common mappings: `image/jpeg` → `.jpg/.jpeg`, `image/png` → `.png`, `application/pdf` → `.pdf`, etc.
   - Prevent MIME type spoofing (mismatched extension and MIME type)

3. **File Size Validation**: Enforce maximum file size
   - Default limit: 10 MB (10,485,760 bytes)
   - Configurable per instance
   - Reject files exceeding the limit

4. **Filename Sanitization**: Clean and secure filenames
   - Remove or replace dangerous characters
   - Prevent path traversal (no `..`, `/`, `\`)
   - Handle unicode characters safely
   - Limit filename length (max 255 characters)
   - Handle empty or whitespace-only names

5. **Unique Filename Generation**: Create collision-free storage names
   - Generate unique identifier for each file
   - Preserve original extension
   - Format: `{unique_id}_{sanitized_original_name}.{ext}`
   - Ensure no filename collisions

**Technical Specifications:**
- Return validation results as a dictionary with success/failure and messages
- Use `secrets` module for generating unique identifiers
- Handle edge cases gracefully (empty names, all special chars, etc.)
- Provide clear error messages for validation failures

---

## Background Topics

### Why File Upload Validation Matters

File upload vulnerabilities are among the most dangerous web security issues:
- **Remote Code Execution**: Uploading executable files (`.php`, `.jsp`, `.exe`) can allow attackers to run code on the server
- **Path Traversal**: Filenames like `../../etc/passwd` can write files outside intended directories
- **Storage Exhaustion**: Large files can fill disk space (DoS attack)
- **MIME Type Confusion**: Browsers may execute files based on content type, not extension
- **XSS via SVG**: SVG files can contain JavaScript

### Common Attack Vectors

1. **Double Extension**: `malicious.php.jpg` - some systems only check last extension
2. **Null Byte Injection**: `malicious.php%00.jpg` - truncates at null byte in some languages
3. **Path Traversal**: `../../../var/www/shell.php` - writes outside upload directory
4. **MIME Type Spoofing**: Send `image/jpeg` MIME type with `.php` file
5. **Unicode Tricks**: `file\u202egnp.exe` (right-to-left override makes it appear as `file.exe.png`)
6. **Case Manipulation**: `file.PhP` to bypass case-sensitive filters

### MIME Types Explained

MIME (Multipurpose Internet Mail Extensions) types identify file content:
- Format: `type/subtype` (e.g., `image/jpeg`, `application/pdf`)
- **Magic Number**: Files have binary signatures at the start (e.g., JPEG starts with `FF D8 FF`)
- **Content-Type Header**: Sent by browsers, but can be manipulated
- **Defense**: Validate both extension AND MIME type

Common MIME types:
- Images: `image/jpeg`, `image/png`, `image/gif`
- Documents: `application/pdf`, `application/msword`, `text/plain`
- Archives: `application/zip`, `application/x-tar`

### Filename Sanitization

Dangerous characters in filenames:
- **Path separators**: `/` and `\` - can navigate directories
- **Path traversal**: `..` - can go up directories
- **Null bytes**: `\0` - can truncate strings in C-based systems
- **Special characters**: `;`, `&`, `|`, `, `` ` `` - shell command injection
- **Whitespace**: Leading/trailing spaces can cause issues
- **Control characters**: Non-printable characters (ASCII 0-31)

Safe approach:
- Allow only alphanumeric, dash, underscore, and dot
- Replace or remove everything else
- Preserve extension separately
