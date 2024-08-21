﻿# BS-PMC-2024-Team10
ברוכים הבאים לפרויקט BS-PMC-2024-Team10 הפרויקט נועד לספק שירותי משלוחים בין אנשים. קובץ ה-README הזה מספק מבט כללי על הפרויקט והוראות להתקנה ושימוש.

תוכן העניינים:
- התקנה
- שימוש
- מבנה הפרויקט

התקנה:
כדי להריץ את פרויקט BS-PMC-2024-Team10 ב-Django, עקוב אחר השלבים הבאים:
- ודא שיש לך Python מותקן. ניתן להוריד את הגרסה האחרונה של Python מהאתר הרשמי של Python.
- שפל את קבצי הפרויקט ממאגר ה-GitHub:

git clone https://github.com/BS-PMC-2024/BS-PMC-2024-Team10.git

- נווט לתיקיית הפרויקט:

cd bs-pmc-2024-team10

- התקן את התלויות של הפרויקט:

pip install -r requirements.txt


- הגדר את מסד הנתונים:
python manage.py migrate

- צור משתמש ראשי (מנהל) במערכת:
python manage.py createsuperuser

- הרץ את שרת הפיתוח:
python manage.py runserver

הפרויקט BS-PMC-2024-Team10 צריך לרוץ כעת בצורה מקומית בכתובת: `http://localhost:8000/`.
