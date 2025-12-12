"""
Google Docs and Sheets API Client.

Usage:
    docs_client = GoogleDocsClient(credentials_path)
    doc_id = docs_client.create_document('My Document', content)
    
    sheets_client = GoogleSheetsClient(credentials_path)
    sheet_id = sheets_client.create_spreadsheet('My Sheet')
"""

import os
from typing import Dict, List, Optional
from google.oauth2.credentials import Credentials
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


class GoogleDocsClient:
    """Client for Google Docs API."""
    
    SCOPES = ['https://www.googleapis.com/auth/documents', 'https://www.googleapis.com/auth/drive']
    
    def __init__(self, credentials_path: Optional[str] = None):
        """
        Initialize Google Docs client.
        
        Args:
            credentials_path: Path to service account JSON or OAuth credentials.
                             If None, reads from GOOGLE_CREDENTIALS_PATH env var.
        """
        creds_path = credentials_path or os.getenv('GOOGLE_CREDENTIALS_PATH')
        if not creds_path:
            raise ValueError("Google credentials path required. Set GOOGLE_CREDENTIALS_PATH env var.")
        
        # Try service account first, then OAuth
        try:
            self.credentials = service_account.Credentials.from_service_account_file(
                creds_path, scopes=self.SCOPES
            )
        except Exception:
            # Check if it's an OAuth client secret file or authorized user file
            import json
            with open(creds_path, 'r') as f:
                creds_data = json.load(f)
            
            # If it has 'installed' or 'web' key, it's a client secret file
            if 'installed' in creds_data or 'web' in creds_data:
                # This is a client secret file - need to do OAuth flow
                from google_auth_oauthlib.flow import InstalledAppFlow
                import pickle
                
                # Check for existing token
                token_path = creds_path.replace('.json', '_token.pickle')
                if os.path.exists(token_path):
                    with open(token_path, 'rb') as token_file:
                        self.credentials = pickle.load(token_file)
                else:
                    # Token file doesn't exist - need OAuth authorization
                    raise Exception(
                        "OAuth token not found. Please run authorization first:\n\n"
                        "  python3 scripts/authorize_google_oauth.py\n\n"
                        "This will open a browser for you to authorize Google APIs access."
                    )
            else:
                # Try as authorized user file
                self.credentials = Credentials.from_authorized_user_file(creds_path, self.SCOPES)
        
        self.docs_service = build('docs', 'v1', credentials=self.credentials)
        self.drive_service = build('drive', 'v3', credentials=self.credentials)
    
    def create_document(self, title: str, content: Optional[List[Dict]] = None, folder_id: Optional[str] = None) -> str:
        """
        Create a new Google Doc.
        
        Args:
            title: Document title
            content: Optional initial content (list of document elements)
            folder_id: Optional folder ID to create document in (from GOOGLE_DRIVE_FOLDER_ID env var if not provided)
            
        Returns:
            Document ID
        """
        try:
            target_folder = folder_id or os.getenv('GOOGLE_DRIVE_FOLDER_ID')
            
            # Check if we're using a service account with no quota
            # If quota error, provide helpful message
            try:
                # Try creating via Docs API first (preferred method)
                doc = self.docs_service.documents().create(body={'title': title}).execute()
                doc_id = doc.get('documentId')
                
                # Move document to specified folder if provided
                if target_folder:
                    try:
                        # Get current parents
                        file = self.drive_service.files().get(fileId=doc_id, fields='parents').execute()
                        previous_parents = ','.join(file.get('parents', []))
                        
                        # Move to target folder
                        self.drive_service.files().update(
                            fileId=doc_id,
                            addParents=target_folder,
                            removeParents=previous_parents,
                            fields='id, parents'
                        ).execute()
                    except Exception as e:
                        print(f"Warning: Could not move document to folder {target_folder}: {e}")
            except HttpError as docs_error:
                error_str = str(docs_error)
                # If Docs API fails, try creating via Drive API
                if '403' in error_str or 'permission' in error_str.lower():
                    # Create via Drive API as fallback
                    file_metadata = {
                        'name': title,
                        'mimeType': 'application/vnd.google-apps.document'
                    }
                    if target_folder:
                        file_metadata['parents'] = [target_folder]
                    
                    try:
                        file = self.drive_service.files().create(
                            body=file_metadata,
                            fields='id'
                        ).execute()
                        doc_id = file.get('id')
                    except HttpError as drive_error:
                        drive_error_str = str(drive_error)
                        if 'storageQuotaExceeded' in drive_error_str or 'quota' in drive_error_str.lower():
                            # Service account has no quota - provide helpful error
                            raise Exception(
                                "Google Drive storage quota exceeded. Service account has 0 GB quota.\n\n"
                                "Solutions:\n"
                                "1. Use OAuth 2.0 credentials instead of service account\n"
                                "2. Request quota increase for service account\n"
                                "3. Use domain-wide delegation (Google Workspace)\n"
                                "4. Create documents manually in Google Drive\n\n"
                                "See GOOGLE-DRIVE-QUOTA-SOLUTION.md for details."
                            )
                        raise
                else:
                    raise
            
            # Add content if provided
            if content:
                self.docs_service.documents().batchUpdate(
                    documentId=doc_id,
                    body={'requests': content}
                ).execute()
            
            return doc_id
        except HttpError as error:
            error_str = str(error)
            if 'storageQuotaExceeded' in error_str or 'quota' in error_str.lower():
                raise Exception(f"Google Drive storage quota exceeded. Please free up space in the shared folder.")
            raise Exception(f"Error creating document: {error}")
    
    def insert_text(self, document_id: str, text: str, index: int = 1) -> None:
        """
        Insert text into document.
        
        Args:
            document_id: Document ID
            text: Text to insert
            index: Character index where to insert (1-based)
        """
        requests = [{
            'insertText': {
                'location': {'index': index},
                'text': text
            }
        }]
        
        self.docs_service.documents().batchUpdate(
            documentId=document_id,
            body={'requests': requests}
        ).execute()
    
    def format_heading(self, document_id: str, start_index: int, end_index: int, level: int = 1) -> None:
        """
        Format text as heading.
        
        Args:
            document_id: Document ID
            start_index: Start character index
            end_index: End character index
            level: Heading level (1-6)
        """
        requests = [{
            'updateParagraphStyle': {
                'range': {
                    'startIndex': start_index,
                    'endIndex': end_index
                },
                'paragraphStyle': {
                    'namedStyleType': f'HEADING_{level}'
                },
                'fields': 'namedStyleType'
            }
        }]
        
        self.docs_service.documents().batchUpdate(
            documentId=document_id,
            body={'requests': requests}
        ).execute()
    
    def create_table(self, document_id: str, rows: int, columns: int, start_index: int = 1) -> Dict:
        """
        Create a table in document.
        
        Args:
            document_id: Document ID
            rows: Number of rows
            columns: Number of columns
            start_index: Character index where to insert table
            
        Returns:
            Table creation result
        """
        requests = [{
            'insertTable': {
                'location': {'index': start_index},
                'rows': rows,
                'columns': columns
            }
        }]
        
        result = self.docs_service.documents().batchUpdate(
            documentId=document_id,
            body={'requests': requests}
        ).execute()
        
        return result
    
    def share_document(self, document_id: str, email: str, role: str = 'writer') -> None:
        """
        Share document with user.
        
        Args:
            document_id: Document ID
            email: Email address to share with
            role: Permission role ('reader', 'writer', 'commenter')
        """
        permission = {
            'type': 'user',
            'role': role,
            'emailAddress': email
        }
        
        self.drive_service.permissions().create(
            fileId=document_id,
            body=permission
        ).execute()
    
    def get_document_url(self, document_id: str) -> str:
        """Get shareable URL for document."""
        return f"https://docs.google.com/document/d/{document_id}/edit"


class GoogleSheetsClient:
    """Client for Google Sheets API."""
    
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
    
    def __init__(self, credentials_path: Optional[str] = None):
        """
        Initialize Google Sheets client.
        
        Args:
            credentials_path: Path to service account JSON or OAuth credentials.
                             If None, reads from GOOGLE_CREDENTIALS_PATH env var.
        """
        creds_path = credentials_path or os.getenv('GOOGLE_CREDENTIALS_PATH')
        if not creds_path:
            raise ValueError("Google credentials path required. Set GOOGLE_CREDENTIALS_PATH env var.")
        
        try:
            self.credentials = service_account.Credentials.from_service_account_file(
                creds_path, scopes=self.SCOPES
            )
        except Exception:
            self.credentials = Credentials.from_authorized_user_file(creds_path, self.SCOPES)
        
        self.sheets_service = build('sheets', 'v4', credentials=self.credentials)
        self.drive_service = build('drive', 'v3', credentials=self.credentials)
    
    def create_spreadsheet(self, title: str, folder_id: Optional[str] = None) -> str:
        """
        Create a new spreadsheet.
        
        Args:
            title: Spreadsheet title
            folder_id: Optional folder ID to create spreadsheet in (from GOOGLE_DRIVE_FOLDER_ID env var if not provided)
            
        Returns:
            Spreadsheet ID
        """
        spreadsheet = {
            'properties': {
                'title': title
            }
        }
        
        spreadsheet = self.sheets_service.spreadsheets().create(
            body=spreadsheet,
            fields='spreadsheetId'
        ).execute()
        
        sheet_id = spreadsheet.get('spreadsheetId')
        
        # Move spreadsheet to specified folder if provided
        target_folder = folder_id or os.getenv('GOOGLE_DRIVE_FOLDER_ID')
        if target_folder:
            try:
                # Get current parents
                file = self.drive_service.files().get(fileId=sheet_id, fields='parents').execute()
                previous_parents = ','.join(file.get('parents', []))
                
                # Move to target folder
                self.drive_service.files().update(
                    fileId=sheet_id,
                    addParents=target_folder,
                    removeParents=previous_parents,
                    fields='id, parents'
                ).execute()
            except Exception as e:
                print(f"Warning: Could not move spreadsheet to folder {target_folder}: {e}")
                # Continue anyway - spreadsheet was created
        
        return sheet_id
    
    def create_sheet(self, spreadsheet_id: str, sheet_name: str) -> None:
        """
        Create a new sheet/tab in spreadsheet.
        
        Args:
            spreadsheet_id: Spreadsheet ID
            sheet_name: Name of new sheet
        """
        requests = [{
            'addSheet': {
                'properties': {
                    'title': sheet_name
                }
            }
        }]
        
        self.sheets_service.spreadsheets().batchUpdate(
            spreadsheetId=spreadsheet_id,
            body={'requests': requests}
        ).execute()
    
    def write_values(self, spreadsheet_id: str, range_name: str, values: List[List]) -> None:
        """
        Write values to sheet.
        
        Args:
            spreadsheet_id: Spreadsheet ID
            range_name: A1 notation range (e.g., 'Sheet1!A1:B2')
            values: 2D list of values
        """
        body = {
            'values': values
        }
        
        self.sheets_service.spreadsheets().values().update(
            spreadsheetId=spreadsheet_id,
            range=range_name,
            valueInputOption='USER_ENTERED',
            body=body
        ).execute()
    
    def set_formula(self, spreadsheet_id: str, cell: str, formula: str) -> None:
        """
        Set formula in cell.
        
        Args:
            spreadsheet_id: Spreadsheet ID
            cell: Cell reference (e.g., 'Sheet1!A1')
            formula: Formula string (without =)
        """
        requests = [{
            'updateCells': {
                'range': {
                    'sheetId': 0,  # Will need to get actual sheet ID
                    'startRowIndex': 0,
                    'startColumnIndex': 0
                },
                'rows': [{
                    'values': [{
                        'userEnteredValue': {
                            'formulaValue': f'={formula}'
                        }
                    }]
                }],
                'fields': 'userEnteredValue'
            }
        }]
        
        # This is simplified - need proper cell parsing
        self.sheets_service.spreadsheets().batchUpdate(
            spreadsheetId=spreadsheet_id,
            body={'requests': requests}
        ).execute()
    
    def format_header_row(self, spreadsheet_id: str, sheet_id: int, row: int = 0) -> None:
        """
        Format header row (bold, background color).
        
        Args:
            spreadsheet_id: Spreadsheet ID
            sheet_id: Sheet ID
            row: Row index (0-based)
        """
        requests = [{
            'repeatCell': {
                'range': {
                    'sheetId': sheet_id,
                    'startRowIndex': row,
                    'endRowIndex': row + 1
                },
                'cell': {
                    'userEnteredFormat': {
                        'backgroundColor': {
                            'red': 0.9,
                            'green': 0.9,
                            'blue': 0.9
                        },
                        'textFormat': {
                            'bold': True
                        }
                    }
                },
                'fields': 'userEnteredFormat(backgroundColor,textFormat)'
            }
        }]
        
        self.sheets_service.spreadsheets().batchUpdate(
            spreadsheetId=spreadsheet_id,
            body={'requests': requests}
        ).execute()
    
    def freeze_rows(self, spreadsheet_id: str, sheet_id: int, rows: int = 1) -> None:
        """
        Freeze header rows.
        
        Args:
            spreadsheet_id: Spreadsheet ID
            sheet_id: Sheet ID
            rows: Number of rows to freeze
        """
        requests = [{
            'updateSheetProperties': {
                'properties': {
                    'sheetId': sheet_id,
                    'gridProperties': {
                        'frozenRowCount': rows
                    }
                },
                'fields': 'gridProperties.frozenRowCount'
            }
        }]
        
        self.sheets_service.spreadsheets().batchUpdate(
            spreadsheetId=spreadsheet_id,
            body={'requests': requests}
        ).execute()
    
    def get_spreadsheet_url(self, spreadsheet_id: str) -> str:
        """Get shareable URL for spreadsheet."""
        return f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}/edit"


if __name__ == '__main__':
    # Example usage
    print("Google API clients initialized")
    print("Use these classes to interact with Google Docs and Sheets")
