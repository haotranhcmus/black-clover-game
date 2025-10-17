# 🎮 Black Clover Game

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Pygame](https://img.shields.io/badge/Pygame-Required-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

_Một trò chơi phiêu lưu hành động kết hợp platformer và endless runner_

[Giới thiệu](#giới-thiệu) •
[Tính năng](#tính-năng) •
[Cài đặt](#cài-đặt) •
[Cách chơi](#cách-chơi) •
[Điều khiển](#điều-khiển)

</div>

---

## 📖 Giới thiệu

**Black Clover Game** là một trò chơi kết hợp giữa hai thể loại:

- **Platformer** (như Mario, Contra)
- **Endless Runner** (như Temple Run)

### 🎬 Câu chuyện

Bạn vào vai một pháp sư bị giam trong ngục tối hắc ám. Ngục tù đang dần sụp đổ và bạn phải thoát ra trước khi quá muộn! Trên đường chạy thoát, vô số quái vật nguy hiểm đang chờ đợi. Sử dụng ma pháp của mình để chiến đấu hoặc khéo léo né tránh chúng để sinh tồn!

> 💡 Ý tưởng lấy cảm hứng từ: https://youtu.be/ObEOK7HSq2E?si=bkOMaWAjfFJw4zqr

---

## ✨ Tính năng

- 🎲 **Level ngẫu nhiên vô tận**: Game tự động tạo các level từ 15 bản đồ được thiết kế sẵn
- 🤖 **AI quái vật thông minh**: Quái vật tự di chuyển và tấn công khi phát hiện người chơi
- 🎨 **Animation mượt mà**: Mỗi nhân vật có animation riêng cho từng trạng thái (chạy, nhảy, rơi, tấn công...)
- 🔊 **Âm thanh sống động**: Nhạc nền và hiệu ứng âm thanh cho mọi hành động
- 📊 **Hệ thống điểm số**: Điểm được tính dựa trên quãng đường bạn vượt qua
- ⚔️ **Hệ thống chiến đấu**: Sử dụng ma pháp để tiêu diệt quái vật
- ❤️ **Thanh máu và mana**: Quản lý tài nguyên để sinh tồn
- 💎 **Vật phẩm thu thập**: Nhặt ruby, vàng và items hồi máu

---

## 🚀 Cài đặt

### Yêu cầu hệ thống

- Python 3.8 trở lên
- Pygame

### Hướng dẫn cài đặt

1. **Clone repository:**

```bash
git clone git@github.com:haotranhcmus/black-clover-game.git
```

2. **Di chuyển vào thư mục dự án:**

```bash
cd black-clover-game
```

3. **Cài đặt dependencies:**

```bash
pip install pygame
```

Hoặc sử dụng file requirements:

```bash
pip install -r requirements.txt
```

4. **Chạy game:**

```bash
python3 main.py
```

---

## 🎮 Cách chơi

1. Khởi động game bằng lệnh `python3 main.py`
2. Chọn **Start** từ menu chính
3. Điều khiển pháp sư của bạn để:
   - ⚔️ Tiêu diệt quái vật bằng ma pháp
   - 🏃 Né tránh chướng ngại vật
   - 💎 Thu thập vật phẩm
   - 📏 Đi càng xa càng tốt để ghi điểm cao

---

## ⌨️ Điều khiển

| Phím    | Chức năng           |
| ------- | ------------------- |
| `←`     | Di chuyển sang trái |
| `→`     | Di chuyển sang phải |
| `Space` | Nhảy                |
| `A`     | Tấn công phép thuật |
| `ESC`   | Tạm dừng / Menu     |

---

## 📂 Cấu trúc dự án

```
📦 black-clover-game
├── 📄 main.py              # File chính để chạy game
├── 📄 Player.py            # Class nhân vật người chơi
├── 📄 Monster.py           # Class quái vật
├── 📄 World.py             # Class quản lý thế giới game
├── 📄 HealthBar.py         # Thanh máu
├── 📄 ManaBar.py           # Thanh mana
├── 📁 assest/              # Hình ảnh nhân vật, quái vật
├── 📁 map/                 # Dữ liệu các level
├── 📁 sound/               # Âm thanh và nhạc nền
├── 📁 img/                 # Hình ảnh UI, button
└── 📄 requirements.txt     # Danh sách thư viện cần thiết
```

---

## 🛠️ Công nghệ sử dụng

- **Python 3**: Ngôn ngữ lập trình chính
- **Pygame**: Thư viện phát triển game 2D

---

## 📝 License

Dự án này được phát hành dưới giấy phép MIT.

---

## 👨‍💻 Tác giả

Được phát triển bởi **Hao Tran**

- GitHub: [@haotranhcmus](https://github.com/haotranhcmus)

---

<div align="center">

**⭐ Nếu bạn thích game này, hãy cho một star nhé! ⭐**

_Chúc bạn chơi game vui vẻ!_ 🎮

</div>

<img width="1291" height="716" alt="image" src="https://github.com/user-attachments/assets/1d260833-7fcb-40d2-bfc1-4d484c872725" />
<img width="1291" height="716" alt="image" src="https://github.com/user-attachments/assets/93032165-984a-4a36-bfdc-64149309d47a" />
<img width="1291" height="716" alt="image" src="https://github.com/user-attachments/assets/fbb2ca5e-1b09-4272-8c7c-5a813ad8015b" />
<img width="1291" height="716" alt="image" src="https://github.com/user-attachments/assets/fc04670f-6372-4b17-ae1f-86607bc54359" />
<img width="1291" height="716" alt="image" src="https://github.com/user-attachments/assets/b9c8e19f-166f-42d6-8d8b-8ca377454db9" />







