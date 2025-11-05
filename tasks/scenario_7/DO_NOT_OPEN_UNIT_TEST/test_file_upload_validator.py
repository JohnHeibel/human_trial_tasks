import unittest
from canonical_solution import FileUploadValidator


class TestFileUploadValidator(unittest.TestCase):
    """Test suite for file upload validator."""

    def setUp(self):
        """Set up test fixtures."""
        self.validator = FileUploadValidator()

    # Extension validation tests

    def test_validate_extension_allowed_jpg(self):
        """Test that .jpg extension is allowed."""
        result = self.validator.validate_extension('photo.jpg')
        self.assertTrue(result['valid'])

    def test_validate_extension_allowed_png(self):
        """Test that .png extension is allowed."""
        result = self.validator.validate_extension('image.png')
        self.assertTrue(result['valid'])

    def test_validate_extension_allowed_pdf(self):
        """Test that .pdf extension is allowed."""
        result = self.validator.validate_extension('document.pdf')
        self.assertTrue(result['valid'])

    def test_validate_extension_case_insensitive(self):
        """Test that extension checking is case-insensitive."""
        self.assertTrue(self.validator.validate_extension('photo.JPG')['valid'])
        self.assertTrue(self.validator.validate_extension('photo.Jpg')['valid'])
        self.assertTrue(self.validator.validate_extension('photo.PNG')['valid'])

    def test_validate_extension_dangerous(self):
        """Test that dangerous extensions are rejected."""
        dangerous = ['malware.exe', 'script.sh', 'hack.bat', 'backdoor.php', 'virus.js']
        for filename in dangerous:
            result = self.validator.validate_extension(filename)
            self.assertFalse(result['valid'], f'{filename} should be rejected')

    def test_validate_extension_no_extension(self):
        """Test that files without extensions are rejected."""
        result = self.validator.validate_extension('noextension')
        self.assertFalse(result['valid'])

    def test_validate_extension_empty_filename(self):
        """Test that empty filenames are rejected."""
        result = self.validator.validate_extension('')
        self.assertFalse(result['valid'])

    # MIME type validation tests

    def test_validate_mime_type_jpeg_match(self):
        """Test MIME type validation for JPEG."""
        result = self.validator.validate_mime_type('photo.jpg', 'image/jpeg')
        self.assertTrue(result['valid'])

        result = self.validator.validate_mime_type('photo.jpeg', 'image/jpeg')
        self.assertTrue(result['valid'])

    def test_validate_mime_type_png_match(self):
        """Test MIME type validation for PNG."""
        result = self.validator.validate_mime_type('image.png', 'image/png')
        self.assertTrue(result['valid'])

    def test_validate_mime_type_pdf_match(self):
        """Test MIME type validation for PDF."""
        result = self.validator.validate_mime_type('doc.pdf', 'application/pdf')
        self.assertTrue(result['valid'])

    def test_validate_mime_type_mismatch(self):
        """Test that mismatched MIME type and extension is rejected."""
        # PNG file claiming to be JPEG
        result = self.validator.validate_mime_type('image.png', 'image/jpeg')
        self.assertFalse(result['valid'])

        # PDF file claiming to be image
        result = self.validator.validate_mime_type('doc.pdf', 'image/png')
        self.assertFalse(result['valid'])

    def test_validate_mime_type_not_allowed(self):
        """Test that disallowed MIME types are rejected."""
        result = self.validator.validate_mime_type('file.txt', 'application/x-executable')
        self.assertFalse(result['valid'])

    # File size validation tests

    def test_validate_file_size_acceptable(self):
        """Test that files under the limit are accepted."""
        result = self.validator.validate_file_size(1024)  # 1 KB
        self.assertTrue(result['valid'])

        result = self.validator.validate_file_size(5242880)  # 5 MB
        self.assertTrue(result['valid'])

    def test_validate_file_size_at_limit(self):
        """Test file exactly at size limit."""
        result = self.validator.validate_file_size(10485760)  # Exactly 10 MB
        self.assertTrue(result['valid'])

    def test_validate_file_size_exceeds_limit(self):
        """Test that files over the limit are rejected."""
        result = self.validator.validate_file_size(10485761)  # 1 byte over 10 MB
        self.assertFalse(result['valid'])

        result = self.validator.validate_file_size(20971520)  # 20 MB
        self.assertFalse(result['valid'])

    def test_validate_file_size_empty(self):
        """Test that empty files are rejected."""
        result = self.validator.validate_file_size(0)
        self.assertFalse(result['valid'])

    def test_validate_file_size_negative(self):
        """Test that negative sizes are rejected."""
        result = self.validator.validate_file_size(-1)
        self.assertFalse(result['valid'])

    def test_validate_file_size_custom_limit(self):
        """Test validator with custom size limit."""
        small_validator = FileUploadValidator(max_size_bytes=1048576)  # 1 MB

        result = small_validator.validate_file_size(524288)  # 512 KB - OK
        self.assertTrue(result['valid'])

        result = small_validator.validate_file_size(2097152)  # 2 MB - Too large
        self.assertFalse(result['valid'])

    # Filename sanitization tests

    def test_sanitize_filename_basic(self):
        """Test basic filename sanitization."""
        result = self.validator.sanitize_filename('document.pdf')
        self.assertEqual(result, 'document.pdf')

    def test_sanitize_filename_spaces(self):
        """Test that spaces are replaced with underscores."""
        result = self.validator.sanitize_filename('my document.pdf')
        self.assertEqual(result, 'my_document.pdf')

    def test_sanitize_filename_special_chars(self):
        """Test that special characters are removed/replaced."""
        result = self.validator.sanitize_filename('file@#$%name!.pdf')
        # Special chars should be replaced with underscores
        self.assertNotIn('@', result)
        self.assertNotIn('#', result)
        self.assertNotIn('$', result)
        self.assertNotIn('%', result)
        self.assertNotIn('!', result)
        self.assertTrue(result.endswith('.pdf'))

    def test_sanitize_filename_path_traversal(self):
        """Test that path traversal attempts are prevented."""
        result = self.validator.sanitize_filename('../../etc/passwd.txt')
        self.assertNotIn('..', result)
        self.assertNotIn('/', result)
        # Should only have the filename part
        self.assertTrue(result.endswith('.txt'))

    def test_sanitize_filename_windows_path(self):
        """Test that Windows paths are sanitized."""
        result = self.validator.sanitize_filename('C:\\Windows\\System32\\file.pdf')
        self.assertNotIn('\\', result)
        self.assertNotIn(':', result)
        self.assertTrue(result.endswith('.pdf'))

    def test_sanitize_filename_null_bytes(self):
        """Test that null bytes are removed."""
        result = self.validator.sanitize_filename('file\x00.pdf')
        self.assertNotIn('\x00', result)

    def test_sanitize_filename_empty(self):
        """Test that empty filenames get default name."""
        result = self.validator.sanitize_filename('')
        self.assertEqual(result, 'unnamed')

    def test_sanitize_filename_only_special_chars(self):
        """Test filename with only special characters."""
        result = self.validator.sanitize_filename('!@#$%^&*().pdf')
        # Should have some valid name and extension
        self.assertTrue(result.endswith('.pdf'))
        self.assertGreater(len(result), 4)  # More than just '.pdf'

    def test_sanitize_filename_unicode(self):
        """Test that unicode characters are handled."""
        result = self.validator.sanitize_filename('файл.pdf')
        # Non-ASCII should be replaced
        self.assertTrue(result.endswith('.pdf'))
        # Should have sanitized the unicode characters
        self.assertTrue(all(ord(c) < 128 for c in result.replace('.pdf', '')))

    def test_sanitize_filename_long(self):
        """Test that very long filenames are truncated."""
        long_name = 'a' * 300 + '.pdf'
        result = self.validator.sanitize_filename(long_name)
        # Should be truncated but keep extension
        self.assertLess(len(result), 256)
        self.assertTrue(result.endswith('.pdf'))

    # Unique filename generation tests

    def test_generate_unique_filename_format(self):
        """Test that generated filenames have correct format."""
        result = self.validator.generate_unique_filename('document.pdf')

        # Should contain underscore separator
        self.assertIn('_', result)

        # Should end with .pdf
        self.assertTrue(result.endswith('.pdf'))

        # Should start with hex characters (unique ID)
        parts = result.split('_', 1)
        self.assertTrue(all(c in '0123456789abcdef' for c in parts[0]))

    def test_generate_unique_filename_preserves_extension(self):
        """Test that original extension is preserved."""
        extensions = ['.jpg', '.png', '.pdf', '.txt', '.docx']

        for ext in extensions:
            result = self.validator.generate_unique_filename(f'file{ext}')
            self.assertTrue(result.endswith(ext))

    def test_generate_unique_filename_sanitizes(self):
        """Test that generated filenames are sanitized."""
        result = self.validator.generate_unique_filename('../../dangerous file!.pdf')

        # Should not contain dangerous characters
        self.assertNotIn('..', result)
        self.assertNotIn('/', result)
        self.assertNotIn('!', result)

    # Complete validation tests

    def test_validate_upload_success(self):
        """Test successful file upload validation."""
        result = self.validator.validate_upload(
            filename='photo.jpg',
            file_size_bytes=2097152,  # 2 MB
            mime_type='image/jpeg'
        )

        self.assertTrue(result['valid'])
        self.assertIsNotNone(result['safe_filename'])
        self.assertEqual(len(result['errors']), 0)
        self.assertTrue(result['safe_filename'].endswith('.jpg'))

    def test_validate_upload_invalid_extension(self):
        """Test upload rejection due to invalid extension."""
        result = self.validator.validate_upload(
            filename='malware.exe',
            file_size_bytes=1024,
            mime_type='application/x-executable'
        )

        self.assertFalse(result['valid'])
        self.assertIsNone(result['safe_filename'])
        self.assertGreater(len(result['errors']), 0)

    def test_validate_upload_mime_mismatch(self):
        """Test upload rejection due to MIME type mismatch."""
        result = self.validator.validate_upload(
            filename='image.png',
            file_size_bytes=1024,
            mime_type='image/jpeg'  # Wrong MIME type
        )

        self.assertFalse(result['valid'])
        self.assertIn('mime_type', result['details'])
        self.assertFalse(result['details']['mime_type']['valid'])

    def test_validate_upload_too_large(self):
        """Test upload rejection due to file size."""
        result = self.validator.validate_upload(
            filename='huge.jpg',
            file_size_bytes=20971520,  # 20 MB
            mime_type='image/jpeg'
        )

        self.assertFalse(result['valid'])
        self.assertIn('file_size', result['details'])
        self.assertFalse(result['details']['file_size']['valid'])

    def test_validate_upload_multiple_errors(self):
        """Test upload with multiple validation failures."""
        result = self.validator.validate_upload(
            filename='malware.exe',
            file_size_bytes=20971520,
            mime_type='application/x-executable'
        )

        self.assertFalse(result['valid'])
        # Should have multiple errors
        self.assertGreater(len(result['errors']), 1)

    def test_validate_upload_details_structure(self):
        """Test that validation result has correct structure."""
        result = self.validator.validate_upload(
            filename='test.pdf',
            file_size_bytes=1024,
            mime_type='application/pdf'
        )

        # Check structure
        self.assertIn('valid', result)
        self.assertIn('safe_filename', result)
        self.assertIn('errors', result)
        self.assertIn('details', result)

        # Check details has all validations
        self.assertIn('extension', result['details'])
        self.assertIn('mime_type', result['details'])
        self.assertIn('file_size', result['details'])

    def test_validate_upload_various_valid_files(self):
        """Test validation of various valid file types."""
        valid_uploads = [
            ('photo.jpg', 1024000, 'image/jpeg'),
            ('image.png', 2048000, 'image/png'),
            ('animation.gif', 512000, 'image/gif'),
            ('document.pdf', 3072000, 'application/pdf'),
            ('notes.txt', 10240, 'text/plain'),
            ('report.doc', 2048000, 'application/msword'),
            ('presentation.docx', 4096000, 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'),
        ]

        for filename, size, mime in valid_uploads:
            result = self.validator.validate_upload(filename, size, mime)
            self.assertTrue(result['valid'], f'{filename} should be valid')
            self.assertIsNotNone(result['safe_filename'])

    def test_validate_upload_path_traversal_attack(self):
        """Test that path traversal attacks are handled safely."""
        result = self.validator.validate_upload(
            filename='../../etc/passwd.txt',
            file_size_bytes=1024,
            mime_type='text/plain'
        )

        # Should still validate (extension is valid)
        # But safe_filename should have no path traversal
        if result['valid']:
            self.assertNotIn('..', result['safe_filename'])
            self.assertNotIn('/', result['safe_filename'])

    def test_double_extension(self):
        """Test handling of double extensions."""
        result = self.validator.validate_upload(
            filename='malicious.php.jpg',
            file_size_bytes=1024,
            mime_type='image/jpeg'
        )

        # Should check the LAST extension (.jpg)
        self.assertTrue(result['valid'])
        self.assertTrue(result['safe_filename'].endswith('.jpg'))

    def test_sanitize_preserves_allowed_characters(self):
        """Test that allowed characters in filenames are preserved."""
        result = self.validator.sanitize_filename('my-document_2024.pdf')
        # Dashes, underscores, and alphanumeric should be kept
        self.assertIn('-', result)
        self.assertIn('_', result)
        self.assertIn('2024', result)
        self.assertTrue(result.endswith('.pdf'))

    def test_edge_case_only_extension(self):
        """Test filename that is only an extension."""
        result = self.validator.sanitize_filename('.pdf')
        # Should get a default name
        self.assertTrue(result.endswith('.pdf'))
        self.assertGreater(len(result), 4)  # More than just '.pdf'


if __name__ == '__main__':
    unittest.main()
