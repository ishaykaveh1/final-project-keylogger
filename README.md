# פרויקט KeyLogger: תיעוד

## מבוא
פרויקט זה מציג את מערכת KeyLogger מדומה, המיועדת למטרות לימודיות בלבד. המערכת כוללת שלושה רכיבים עיקריים:
- **KeyLogger Agent**: תוכנה הרצה על מחשב היעד, אוספת הקשות מקלדת, מצפינה אותם ושולחת לשרת.
- **KeyLogger Server (Backend)**: שרת מבוסס Flask המקבל, מפענח ושומר את הנתונים.
- **KeyLogger Explorer (Frontend)**: ממשק אינטרנט להצגת הנתונים שנאספו.

**אזהרה משפטית ואתית:**  
השימוש בפרויקט זה מוגבל לסביבות לימודיות מבוקרות (כגון מכונות וירטואליות או מחשבים אישיים עם אישור). אסור להשתמש בכלי זה לצרכים בלתי חוקיים או לא אתיים, והמשתמשים חייבים להקפיד על חוקי פרטיות ואתיקה מקצועית.

## מבנה המערכת
התרשים הבא מתאר את זרימת המידע:
```
[KeyLogger Agent] --> [KeyLogger Server (Backend)] <--> [KeyLogger Explorer (Frontend)]
```
- **Agent**: אוסף נתונים (הקשות + מידע מערכת), מצפין ושולח לשרת.
- **Backend**: שומר נתונים בתיקיות לפי שם המחשב (hostname).
- **Frontend**: מציג רשימת מחשבים ותוכן הקבצים דרך דפדפן.

## עיצוב (Design)
- **KeyLogger Agent**: 
  - איסוף הקשות באמצעות KeyLoggerService.
  - כתיבה מקומית ו/או שליחה לשרת דרך FileWriter ו-NetworkWriter.
- **חלוקת אחריות**: 
  - KeyLoggerService מטפל באיסוף.
  - FileWriter/ NetworkWriter מנהלים כתיבה ושליחה.

## רכיבים עיקריים
### 1. KeyLogger Agent
- **קבצים:** `systeminfo.py`, `writer.py`, `sender.py`.
- **תפקיד:** אוסף מידע מערכת (OS, חומרה, רשת), מצפין ומשדר לשרת.

### 2. KeyLogger Server (Backend)
- **קובץ:** `backend1.py`.
- **תפקיד:** מקבל נתונים מוצפנים, מפענח, שומר בקבצים (`log_YYYY-MM-DD_HH-MM-SS.txt`) בתיקיית `data/<hostname>/`.
- **נקודות קצה:**
  - `/`: בדיקת שרת.
  - `/data`: רשימת מחשבים.
  - `/data/<name>`: תוכן קבצי מחשב.
  - `/api/upload` (POST): קליטת נתונים.

### 3. KeyLogger Explorer (Frontend)
- **קבצים:** `index.html`, `styles.css`, `scripts.js`.
- **תפקיד:** מציג רשימת מחשבים ותוכן הקבצים דרך AJAX.
- **הערות:** דורש Backend פעיל על `http://127.0.0.1:5000`.

## התקנה והרצה
1. **סביבה:** Python 3.8+.
2. **תלות:** 
   ```
   pip install flask flask-cors psutil requests
   ```
   (מודול `encryption` נדרש ליישום נפרד).
3. **הגדרה:**
   - צור תיקיית `data` (אוטומטי עם הרצת Backend).
   - עדכן `server_url` ב-`sender.py` אם נדרש.
4. **הרצה:**
   - Backend: `python backend1.py`.
   - Agent: `python main_agent.py` (צור קובץ מאחד).
   - Frontend: פתח `index.html` בדפדפן.
5. **בדיקה:** שלח נתונים מה-Agent, בדוק ב-`data/`, וצפה ב-Frontend.

## שימוש
- הרץ Backend.
- הפעל Agent על מחשב יעד.
- גש ל-Frontend, בחר מחשב וצפה בלוגים.
- דוגמה לנתונים: הקשות, מידע מערכת (IP, CPU, זיכרון).

CC BY-NC-SA 4.0 (ייחוס, לא מסחרי, שיתוף זהה).

תאריך עדכון: 08/09/2025, 15:34 IDT.
