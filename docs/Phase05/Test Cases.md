# Test Cases


| ID | Test Case Name | Predictions | Input/Action | Expected Result | Actual Result | (✅/❌) | Notes | Image |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **01** | Add Assignment - Valid Input | App will accept the input and create assignment entry | Class Name: "Chemistry" - Assignment Name: "Balance Equation" - Category: "Equations" - Due Date: “07-07-2027” Notes: "Use the periodic table"| Assignment appears in the list | The assignment appeared on the list |✅| success | <img width="1082" height="687" alt="image" src="https://github.com/user-attachments/assets/8cc0c423-f4ab-4dd6-9e55-8b6215a88903" /><img width="761" height="745" alt="image" src="https://github.com/user-attachments/assets/f567f309-88cc-46e0-8fbd-9692dee303fd" /> |
| **02** | Add Assignment — Invalid Date Format | App will force a valid date format (mm/dd/yyyy) for due date | Class Name: "Math" - Assignment Name: "Math Stuff" - Category: "Math" - Due Date: “2027-07-07” | App will not allow invalid date entry | App crashed |❌| While the app tried to force the correct date format, it still allowed the date to be entered incorrectly and crashed the application | <img width="583" height="679" alt="image" src="https://github.com/user-attachments/assets/0fdf4370-917e-41fe-a9e7-0314aa166ff8" /> |
| **03** | Mark Assignment as Done | Assignment status will be changed from "Not done" to "Done" | An assignment which is currently not done will be marked as "done" by pressing the "Mark done" button | "Not done" -> "Done" | "Not done" -> "Done" |(✅/❌)| Success | <img width="634" height="432" alt="image" src="https://github.com/user-attachments/assets/60c47e70-b029-4a47-a38e-1a5d24b09b3e" /><img width="422" height="411" alt="image" src="https://github.com/user-attachments/assets/77661ce0-8081-4cf2-bc08-3cd0244eb7c2" /> |
| **04** |  |  | |  |  |(✅/❌)|  |  |
| **05** |  |  | |  |  |(✅/❌)|  |  |



