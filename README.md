Bước 1: Đăng nhập vào tài khoản Gemini
Truy cập vào trang web Gemini.

Đăng nhập vào tài khoản của bạn.

Bước 2: Truy cập vào "API Settings"
Trên giao diện chính, bấm vào biểu tượng User Account (biểu tượng hình người) ở góc phải trên cùng.

Chọn Settings → API Settings.

Bước 3: Tạo API Key
Nhấn vào Create New API Key.

Chọn Master API hoặc Sub Account API tùy thuộc vào mục đích sử dụng.

Chọn Scope (Phạm vi):

Primary Account nếu muốn API có quyền truy cập toàn bộ tài khoản.

Sub Account nếu chỉ muốn API quản lý các sub account.

Bước 4: Phân quyền API
Khi tạo API Key, bạn sẽ được yêu cầu chọn các quyền truy cập:

Auditor: Chỉ có thể đọc thông tin.

Trader: Có thể thực hiện giao dịch.

Fund Manager: Có thể nạp/rút tiền.

Custody: Quản lý tài sản lưu ký.

Chọn quyền phù hợp với mục đích sử dụng của bạn.

Bước 5: Xác thực và Lưu trữ API Key
Sau khi hoàn thành, Gemini sẽ cung cấp cho bạn:

API Key

API Secret

API Configuration Details (cấu hình kết nối)

Lưu ý: Lưu trữ các thông tin này an toàn, Gemini chỉ hiển thị API Secret một lần duy nhất sau khi tạo.

Bước 6: Kích hoạt API Key
Gemini sẽ yêu cầu bạn xác nhận qua email để kích hoạt API Key.

Kiểm tra email của bạn và bấm vào link xác nhận.
Bước 7: Tạo file .env GEMINI_API_KEY="your_api_key" truyền api vào để có thể chạy
