Nama : Hafiza Nurul Hidayah
NPM : 2506624101
Kelas : PBP D
Jurusan : Ilmu Komputer

## About this project 
Projek ini merupakan personal portfolio untuk menampilkan beberapa pengalaman, projek, dan background edukasi saya sebagai mahasiswi Fakultas Ilmu Komputer Universitas Indonesia, projek ini juga merupakan salah satu individual assignment dari mata kuliah PBP (Pemrograman Berbasis Platform).

## Project Structure
myportofolio/
├── main/
    |── migrations    
│   ├── models.py
|   ├── ___init__.py
│   ├── views.py
|   ├── admin.py
|   ├── apps.py
|   ├── media.py
│   ├── forms.py
│   ├── urls.py
│   ├── tests.py
|   ├── portofolio.py
|   └── templates/
│        ├── base.html
│        ├── index.html
│        ├── Education.html
│        ├── Education_form.html
│        ├── Experience.html
│        ├── Experience_form.html
│        ├── PreviousWork.html
│        ├── PreviousWork_form.html
│        └── components/
│           └── previous_work_delete_modal.html
│           └── education_delete_modal.html
│           └── experience_delete_modal.html
├── myportofolio/
│   ├── settings.py
│   └── urls.py
├── manage.py
└── requirements.txt

## Cara Menjalankan Project 
python manage.py runserver
http://127.0.0.1:8000/

## Cara Menjalankan Testing
python manage.py test

## Page URL 
1. Halaman Utama : http://127.0.0.1:8000/
2. Halaman Education : http://127.0.0.1:8000/Education/
3. Halaman Experience : http://127.0.0.1:8000/Experience/
4. Halaman Previous Work : http://127.0.0.1:8000/PreviousWork/

## Refleksi AI

AI yang saya gunakan : ChatGpt, Gemini, Claude

Dalam proses pengerjaan tugas ini, saya menggunakan AI sebagai alat bantu untuk memahami konsep dan memeriksa pemahaman saya terhadap beberapa soal. Tapi, saya tetap mencoba untuk mempelajari dan memahami kembali langkah penyelesaian dan konsep yang digunakan agar dapat memahami kode kode yang ada pada file.

Strategi prompting yang saya gunakan adalah mencoba untuk menanyakan beberapa hal yang saya belum tau bagaimana eksekusinya dengan menyertakan referensi atau potongan kode, setelah mendapat penjelasan saya mencoba memahami sendiri dan menanyakan kembali apabila ada yang masih tidak paham. 

Saya menggunakan AI untuk membantu dalam mengatur layout, spacing, ukuran, serta menyesuaikan tampilan website agar lebih responsif pada ukuran desktop dan mobile. Bagian yang paling banyak dibantu AI adalah CSS, terutama ketika saya mengalami kesulitan dalam menentukan penyesuaian layout pada desktop dan mobile. Sementara itu, saya tetap menentukan sendiri struktur HTML, konten website, konsep tampilan, serta membuat wireframe sebagai dasar rancangan website. Selain itu, saya juga meminta bantuan AI untuk menulis commit message yang sekiranya cukup sesuai dengan isi yang saya punya.

Saya juga menggunakan AI untuk memberikan saya penjelasan mengenai instruksi instruksi dan fitur yang ada di django, terkadang saya bingung harus melakukan apa di terminal atau bagaimana caranya melakukan suatu hal tanpa dimasukkan di terminal (contohnya ketika saya ingin menambahkan data untuk education and experience), saya memutuskan untuk nanya ke AI dan juga mencari referensi di internet.

Pada Tugas 4, saya menggunakan AI chatgpt untuk mengimplementasikan authentication, authorization, role Editor, dan fitur Star pada website portfolio saya. Saya cukup sering menggunakan AI untuk memahami konsep yang masih membingungkan, mencari penyebab error, dan mengecek apakah implementasi saya sudah sesuai dengan requirement tugas. Salah satu hal yang paling membantu adalah ketika saya mempelajari perbedaan hak akses antara User, Editor, dan Superuser. 

Saya juga menggunakan AI untuk membantu melakukan debugging pada beberapa bagian Django seperti `login_required`, `PermissionDenied`, Django Group dan Permission, serta penggunaan `ManyToManyField` untuk fitur Star. Namun, setiap solusi tetap saya sesuaikan dengan struktur project saya dan saya uji kembali secara langsung. Dari pengerjaan ini juga, Terkadang solusi yang diberikan AI tidak langsung cocok dengan project saya, sehingga saya harus membaca kembali kode, mencoba sendiri, dan melakukan debugging. 

### Tugas 1
1. Pada kode html yang saya buat saya menggunakan beberapa element yang telah disebutkan di website PBP CS UI, seperti <header> yang saya gunakan untuk bagian judul di website, ;lalu <main> juga saya gunakan untuk highlight main topic / main focus pada halama tersebut, saya juga menggunakan <section> untuk membagi halaman jd bbrp bagian berbeda
sejauh ini penggunaan element semantik sangat membantu saya dalam pembuatan static web karena struktur jadi terlihat lebih rapih dan mudah untuk dipahami.

2. Tantangan yang saya rasa cukup sulit adalah memvisualisasikan bagaimana tata letak setiap kolom yang ada di desktop dapat ditampilkan secara rapih di mobile. Sejujurnya saya tipe orang yang cukup sulit untuk mengatur tata letak secara langsung tanpa membuat wireframe kasar terlebih dahulu, jd saya memutuskan untuk membuat wireframe nya terlebih dahulu supaya lebih mudah untuk memvisualisasikannya. Terkait prioritas saya memprioritaskan element hero seperti pada website saya yaitu bagian about me dan juga navigasi agar bbrp element dapat langsung terlihat dengan cara mengatur tata letak dan juga ukuran. 

3. Setiap kali saya ingin menambahkan informasi di file Index.HTML harus diubah secara manual satu per satu. Hal ini saya rasa kurang efisien dan rentan salah. Untuk fungsionalitas dinamis yang saya harap dapat dipelajari dan ditambahkan untuk proyek selanjutnya adalah penerapan javascript

### Tugas 2
1. saat user mencoba untuk membuka halaman portofolio baru, browser akan mengirimkan request, hal ini pertama kali diterima oleh urls.py yg berfungsi menentukan yang mana yang menangani URL tersebut. lalu, request diteruskan ke urls.py pada main, yang menentukan view yang sesuai berdasarkan URL yang diakses. Setelah itu view akan menjalankan logika untuk mengambil data yang diperlukan dari model. Model sendiri berfungsi sebagai representasi data yang tersimpan di database. Setelah data diperoleh, view mengirimkan data tersebut ke template. Template kemudian menggabungkan struktur HTML dengan data dari model menggunakan Django Template Language. Hasil HTML tersebut dikirim kembali oleh Django ke browser sehingga halaman portofolio beserta datanya dapat dilihat.

2. karena model memungkinkan data dikelola secara terstruktur di dalam database. Dengan cara ini, template hanya bertanggung jawab untuk menampilkan data, sedangkan pengelolaan data dilakukan melalui model. Hal ini membuat app lebih mudah dimaintain dan flexible

3. makemigrations digunakan untuk membuat file migrasi berdasarkan perubahan yang dilakukan pada model. File migrasi tersebut berisi instruksi mengenai perubahan struktur database yang perlu dilakukan. Migrate digunakan untuk menerapkan file migrasi tersebut ke database, sehingga struktur database benar-benar berubah sesuai dengan model terbaru. contoh seperti model saya yaitu education semisal awalnya hanya ada institution, degree, dan year lalu saya ingin menambahkan field baru yaitu achievements. Maka gunakan makemigrations lalu migrate

### Tugas 3
Pada tugas 3 ini saya menambahkan education_form, experience_form, dan previous_work_form dimana pada laman masing masing akan mempunyai fitur untuk mencari berdasarkan keyword, menambahkan (dengan password / security code tertentu), menghapus (dengan password / security code tertentu), dan mengedit / update.

1. Kita menggunakan ModelForm karena ModelForm memungkinkan kita membuat form berdasarkan model Django yang sudah dibuat. Dengan begitu, kita tidak perlu membuat setiap input dan proses penyimpanan data secara manual. Karena modelform secara otomatis menghubungkan field pada form dengan field pada model, melakukan validasi data, dan memudahkan penyimpanan data menggunakan form.save(). Penggunaan ModelForm membuat kode lebih ringkas, terstruktur, dan mengurangi kemungkinan ketidaksesuaian antara form dengan model. {% csrf_token %} digunakan untuk memberikan perlindungan terhadap Cross-Site Request Forgery (CSRF). Token ini memastikan bahwa request POST yang dikirim ke server berasal dari form yang memang dibuat oleh aplikasi kita. Jika form melakukan request POST tanpa CSRF token, Django secara default dapat menolak request tersebut.

2. JSON memiliki struktur dan sintaks yang lebih ringkas dan juga sederhana sehingga ukuran data yang dikirim dapat lebih kecil. JSON juga sangat cocok digunakan untuk komunikasi antara frontend dan backend melalui API, serta dapat langsung direpresentasikan sebagai object/data structure dalam banyak bahasa pemrograman.

3. Client -> request url -> view django -> ambil data dr model (contoh : data = PreviousWork.objects.all()) -> serialization (contoh : serializers.serialize("json", data)) -> data menjadi json -> jsonresponse -> client menerima json (contoh : content_type="application/json").

### Tugas 4 
Pada Tugas 4, portfolio dikembangkan dengan menerapkan sistem autentikasi dan otorisasi menggunakan Django. Pengguna dapat melakukan registrasi, login, dan logout, serta memiliki hak akses yang berbeda berdasarkan perannya. Selain itu, ditambahkan fitur interaktif berupa star pada data portfolio dan peran baru yaitu editor.

## Fitur yang ditambahkan pada tugas 4 ini

### 1. Authentication
Sistem menyediakan fitur:
- Register
- Login
- Logout
- Menampilkan status login
- Menyimpan informasi `last_login` menggunakan cookie

### 2. Profile
Ditambahkan halaman **Profile** yang menampilkan informasi akun pengguna yang sedang digunakan.
Halaman Profile menampilkan:
- Username
- Role pengguna
- Total data portfolio yang di-star
- Daftar Experience yang di-star
- Daftar Education yang di-star
- Daftar Previous Work yang di-star
Profile dapat digunakan untuk melihat aktivitas Star yang dilakukan oleh masing-masing pengguna.

### 3. Role & Authorization
Terdapat 4 jenis akses pengguna:

| Role | Read | Star | Create | Update | Delete |
|------|------|------|--------|--------|--------|
| Visitor | ✅ | ❌ | ❌ | ❌ | ❌ |
| User | ✅ | ✅ | ❌ | ❌ | ❌ |
| Editor | ✅ | ✅ | ❌ | ✅ | ❌ |
| Superuser / Owner | ✅ | ✅ | ✅ | ✅ | ✅ |

Pembatasan akses diterapkan pada **server-side** menggunakan Django authentication dan permission.
Role **Editor** menggunakan Django `Group` dan `Permission`, dengan permission `change` untuk data portfolio.

### 4. Star Feature
Pengguna yang sudah login dapat memberikan atau membatalkan Star pada:
- Experience
- Education
- Previous Work
Fitur Star menggunakan `ManyToManyField` dengan model `User`.
Setiap pengguna hanya dapat memberikan maksimal satu Star pada satu data. Jumlah Star dan status Star pengguna juga ditampilkan pada halaman portfolio.

Aksi Star menggunakan:
- HTTP POST
- CSRF protection
- `login_required`

### 5. Portfolio Data
Portfolio memiliki beberapa bagian:
- Profile
- Experience
- Education
- Previous Work

Pengunjung tetap dapat membaca data portfolio tanpa harus login.

### 6. JSON API
Endpoint JSON dari tugas sebelumnya tetap dipertahankan untuk:
- Experience
- Education
- Previous Work
Data JSON dapat digunakan untuk mengakses data portfolio tanpa mengubah data tersebut.

## Authorization
Pembatasan akses diterapkan pada dua sisi:

### Server-side
View menggunakan:
```python
@login_required