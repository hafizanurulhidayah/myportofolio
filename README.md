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
|           └── previouswork_star.html
│           └── education_star.html
│           └── experience_star.html
|           └── previous_work_form_modal.html
│           └── education_form_modal.html
│           └── experience_form_modal.html
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

## PENGGUNAAN AI TUGAS 1 - TUGAS 5
AI yang saya gunakan : ChatGpt, Gemini, Claude


## REFLEKSI AI TUGAS 1 
Dalam proses pengerjaan tugas ini, saya menggunakan AI sebagai alat bantu untuk memahami konsep dan memeriksa pemahaman saya terhadap beberapa soal. Tapi, saya tetap mencoba untuk mempelajari dan memahami kembali langkah penyelesaian dan konsep yang digunakan agar dapat memahami kode kode yang ada pada file.
Strategi prompting yang saya gunakan adalah mencoba untuk menanyakan beberapa hal yang saya belum tau bagaimana eksekusinya dengan menyertakan referensi atau potongan kode, setelah mendapat penjelasan saya mencoba memahami sendiri dan menanyakan kembali apabila ada yang masih tidak paham. 

## REFELKSI AI TUGAS 2
Saya menggunakan AI untuk membantu dalam mengatur layout, spacing, ukuran, serta menyesuaikan tampilan website agar lebih responsif pada ukuran desktop dan mobile. Bagian yang paling banyak dibantu AI adalah CSS, terutama ketika saya mengalami kesulitan dalam menentukan penyesuaian layout pada desktop dan mobile. Sementara itu, saya tetap menentukan sendiri struktur HTML, konten website, konsep tampilan, serta membuat wireframe sebagai dasar rancangan website. Selain itu, saya juga meminta bantuan AI untuk menulis commit message yang sekiranya cukup sesuai dengan isi yang saya punya.

## REFLEKSI AI TUGAS 3
Saya juga menggunakan AI untuk memberikan saya penjelasan mengenai instruksi instruksi dan fitur yang ada di django, terkadang saya bingung harus melakukan apa di terminal atau bagaimana caranya melakukan suatu hal tanpa dimasukkan di terminal (contohnya ketika saya ingin menambahkan data untuk education and experience), saya memutuskan untuk nanya ke AI dan juga mencari referensi di internet.

## REFLEKSI AI TUGAS 4
Pada Tugas 4, saya menggunakan AI chatgpt untuk mengimplementasikan authentication, authorization, role Editor, dan fitur Star pada website portfolio saya. Saya cukup sering menggunakan AI untuk memahami konsep yang masih membingungkan, mencari penyebab error, dan mengecek apakah implementasi saya sudah sesuai dengan requirement tugas. Salah satu hal yang paling membantu adalah ketika saya mempelajari perbedaan hak akses antara User, Editor, dan Superuser. 

Saya juga menggunakan AI untuk membantu melakukan debugging pada beberapa bagian Django seperti `login_required`, `PermissionDenied`, Django Group dan Permission, serta penggunaan `ManyToManyField` untuk fitur Star. Namun, setiap solusi tetap saya sesuaikan dengan struktur project saya dan saya uji kembali secara langsung. Dari pengerjaan ini juga, Terkadang solusi yang diberikan AI tidak langsung cocok dengan project saya, sehingga saya harus membaca kembali kode, mencoba sendiri, dan melakukan debugging. 

## REFLEKSI AI TUGAS 5
Dalam pengerjaan Tugas 5, saya menggunakan bantuan ChatGPT sebagai AI assistant.
AI digunakan untuk membantu: memahami konsep AJAX, fetch(), async/await, dan debouncing;
membantu menyusun dan memperbaiki implementasi AJAX pada fitur Experience, Education, dan Previous Work, membantu debugging ketika terdapat error pada endpoint, template, form, dan JavaScript, memberikan saran terkait struktur kode dan penamaan commit message, 
membantu menyusun penjelasan dan refleksi untuk README. 

Implementasi akhir, penyesuaian kode dengan proyek, serta proses pengujian tetap saya lakukan dan verifikasi sendiri.

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

### TUGAS 5
Pada Tugas 5, dilakukan pengembangan fitur pada halaman Experience, Education, dan Previous Work dengan menerapkan AJAX untuk mengambil dan menambahkan data secara dinamis tanpa perlu melakukan reload halaman. Saya juga menambahkan kreativitas yaitu melanjutkan tugas 4 dimana pada tugas 4 kreativitas yang saya lakukan adalah menambah page profile, maka pada tugas ini saya menambah toast badge apabila ada pengguna baru yang berhasil menambahkan bintang pertama di kategori experience

## Perubahan yang dilakukan meliputi :
    Mengubah tampilan data Experience, Education, dan Previous Work agar dimuat menggunakan AJAX.
    Menambahkan fitur search menggunakan AJAX sehingga hasil pencarian dapat diperbarui secara langsung tanpa reload halaman.
    Menerapkan debouncing pada fitur pencarian untuk mengurangi jumlah request ke server ketika pengguna sedang mengetik.
    Menambahkan loading state, error state, dan empty state pada halaman.
    Menambahkan fitur menambah Experience, Education, dan Previous Work menggunakan AJAX.
    Menambahkan validasi form dan menampilkan pesan keberhasilan atau kegagalan menggunakan toast notification.
    Menambahkan fitur Security Code pada proses penambahan dan penghapusan data untuk membatasi akses terhadap perubahan data.
    Menambahkan fitur star dan menampilkan jumlah serta pengguna yang memberikan star pada setiap data.
    Menambahkan fitur edit dan delete dengan pembatasan berdasarkan permission/superuser.
    Menggunakan escapeHtml() pada data yang dirender melalui JavaScript untuk membantu mencegah serangan XSS (Cross-Site Scripting).
    Menggunakan fetch() dan async/await untuk melakukan komunikasi asynchronous antara frontend dan backend.
    Menambahkan endpoint AJAX pada Django untuk mengambil dan menambahkan data Experience, Education, dan Previous Work.

## Jawaban Refleksi : 

1. Debouncing adalah teknik pemrograman yang digunakan untuk menunda eksekusi suatu fungsi sampai jangka waktu tertentu berlalu sejak terakhir kali fungsi tersebut dipanggil. 
Mengapa penting untuk fitur pencarian AJAX:
    1. Efisiensi Server: Mencegah pengiriman request HTTP ke server pada setiap ketukan tombol (keystroke). Tanpa debouncing, mengetik kata "laptop" (6 huruf) akan langsung memicu 6 request AJAX sekaligus secara bersamaan.
    2. Optimalisasi Jaringan & Bandwidth: Mengurangi beban lalu lintas jaringan yang tidak perlu akibat request yang berlebihan.
    3. Mencegah Race Conditions: Menghindari masalah di mana respons dari request yang dikirim lebih awal datang terlambat dan menimpa hasil pencarian yang lebih baru.
    Pengalaman Pengguna (UX): Menjaga aplikasi tetap responsif dan mencegah lag atau kedipan antarmuka (UI flickering) akibat render data yang terlalu sering.

2. await: Keyword await digunakan di dalam fungsi async untuk menghentikan sementara eksekusi kode sampai Promise yang dikembalikan oleh fetch() selesai diproses (resolved), sehingga kita bisa mendapatkan objek Response secara berurutan (synchronous-style) sebelum lanjut ke proses parsing data (seperti .json()).
Jika tidak menggunakan await yang akan terjadi adalah : 
    1. JavaScript akan langsung mengeksekusi baris kode berikutnya tanpa menunggu server merespons.
    2. Variabel yang menampung pemanggilan fetch() tidak akan berisi data dari server, melainkan sebuah objek Pending Promise.
    3. Mencoba mengakses atau memproses data (misalnya memanggil .json() atau membaca properti data) langsung dari objek Promise yang belum selesai akan menyebabkan error atau menghasilkan nilai undefined.

3. SS adalah jenis kerentanan keamanan di mana penyerang berhasil menyisipkan skrip berbahaya (biasanya berupa kode JavaScript) ke dalam halaman web yang kemudian dilihat dan dieksekusi di peramban pengguna lain. Serangan ini dapat digunakan untuk mencuri cookie, sesi pengguna, atau memanipulasi tampilan halaman.
Django Templates (Aman secara default): Mesin template bawaan Django secara otomatis melakukan auto-escaping pada variabel yang dirender ke HTML (mengubah karakter khusus seperti <, >, dan & menjadi entitas HTML yang aman), kecuali jika pengembang secara eksplisit menggunakan filter | safe. Sedangkan ajax / javascript lebih rentan karena Ketika data JSON diterima melalui AJAX dan dimasukkan ke dalam DOM menggunakan properti yang tidak aman seperti innerHTML (misalnya element.innerHTML = response.data), peramban akan memperlakukan string tersebut sebagai kode HTML/skrip aktif. Jika data dari server mengandung input pengguna berbahaya yang tidak disanitasi terlebih dahulu, skrip tersebut akan langsung tereksekusi.

