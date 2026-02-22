/**
 * Trilingual dictionary for BaZingSe.
 * All user-facing strings in English / Bahasa Indonesia / 漢字 pīnyīn.
 * No language switching — all 3 displayed together.
 */

export interface TriEntry {
  en: string;
  id: string;
  zh: string;
  py: string; // pinyin
}

/** Full trilingual format: "EN / ID / 漢字 pīnyīn" */
export function tri(e: TriEntry): string {
  return `${e.en} / ${e.id} / ${e.zh} ${e.py}`;
}

/** Compact format for tight spaces: "漢字 EN/ID" */
export function triCompact(e: TriEntry): string {
  if (e.en === e.id) return `${e.zh} ${e.en}`;
  return `${e.zh} ${e.en}/${e.id}`;
}

/** Pillar label format: "漢字 pīnyīn · EN/ID" */
export function triPillar(e: TriEntry): string {
  if (e.en === e.id) return `${e.zh} ${e.py} · ${e.en}`;
  return `${e.zh} ${e.py} · ${e.en}/${e.id}`;
}

// ──────────────────────────────────────────────
// PILLAR LABELS
// ──────────────────────────────────────────────

export const PILLARS = {
  hour:  { en: 'Hour',  id: 'Jam',    zh: '時', py: 'shí' },
  day:   { en: 'Day',   id: 'Hari',   zh: '日', py: 'rì' },
  month: { en: 'Month', id: 'Bulan',  zh: '月', py: 'yuè' },
  year:  { en: 'Year',  id: 'Tahun',  zh: '年', py: 'nián' },
} as const;

export const COMPARISON = {
  hourly:   { en: 'Hourly',   id: 'Per Jam',  zh: '時運', py: 'shí yùn' },
  daily:    { en: 'Daily',    id: 'Harian',   zh: '日運', py: 'rì yùn' },
  monthly:  { en: 'Monthly',  id: 'Bulanan',  zh: '月運', py: 'yuè yùn' },
  annual:   { en: 'Annual',   id: 'Tahunan',  zh: '年運', py: 'nián yùn' },
  ten_year: { en: '10Y',      id: '10Th',     zh: '大運', py: 'dà yùn' },
} as const;

export const TALISMAN = {
  year:  { en: 'T-Year',  id: 'Jimat Tahun', zh: '符年', py: 'fú nián' },
  month: { en: 'T-Month', id: 'Jimat Bulan', zh: '符月', py: 'fú yuè' },
  day:   { en: 'T-Day',   id: 'Jimat Hari',  zh: '符日', py: 'fú rì' },
  hour:  { en: 'T-Hour',  id: 'Jimat Jam',   zh: '符時', py: 'fú shí' },
} as const;

export const LOCATION = {
  overseas_1:   { en: 'Overseas 1',   id: 'Luar Negeri 1',  zh: '海1', py: 'hǎi' },
  overseas_2:   { en: 'Overseas 2',   id: 'Luar Negeri 2',  zh: '海2', py: 'hǎi' },
  birthplace_1: { en: 'Birthplace 1', id: 'Tempat Lahir 1', zh: '鄉1', py: 'xiāng' },
  birthplace_2: { en: 'Birthplace 2', id: 'Tempat Lahir 2', zh: '鄉2', py: 'xiāng' },
  birthplace_3: { en: 'Birthplace 3', id: 'Tempat Lahir 3', zh: '鄉3', py: 'xiāng' },
  birthplace_4: { en: 'Birthplace 4', id: 'Tempat Lahir 4', zh: '鄉4', py: 'xiāng' },
  abroad:       { en: 'Abroad',       id: 'Luar Negeri',    zh: '海外', py: 'hǎiwài' },
  abroad_hint:  { en: 'Overseas location (adds Water element)', id: 'Lokasi luar negeri (menambah elemen Air)', zh: '海外位置（增加水元素）', py: 'hǎiwài wèizhì' },
} as const;

// ──────────────────────────────────────────────
// ACTIONS
// ──────────────────────────────────────────────

export const ACTIONS = {
  delete:   { en: 'Delete',  id: 'Hapus',   zh: '刪除', py: 'shānchú' },
  yes:      { en: 'Yes',     id: 'Ya',      zh: '是',   py: 'shì' },
  no:       { en: 'No',      id: 'Tidak',   zh: '否',   py: 'fǒu' },
  save:     { en: 'Save',    id: 'Simpan',  zh: '保存', py: 'bǎocún' },
  cancel:   { en: 'Cancel',  id: 'Batal',   zh: '取消', py: 'qǔxiāo' },
  create:   { en: 'Create',  id: 'Buat',    zh: '創建', py: 'chuàngjiàn' },
  add:      { en: 'Add',     id: 'Tambah',  zh: '添加', py: 'tiānjiā' },
  enter:    { en: 'Enter',   id: 'Masuk',   zh: '進入', py: 'jìnrù' },
  submit:   { en: 'Submit',  id: 'Kirim',   zh: '提交', py: 'tíjiāo' },
} as const;

// ──────────────────────────────────────────────
// STATUS
// ──────────────────────────────────────────────

export const STATUS = {
  loading:        { en: 'Loading...',       id: 'Memuat...',            zh: '加載中', py: 'jiāzǎi zhōng' },
  loading_chart:  { en: 'Loading chart...', id: 'Memuat grafik...',     zh: '加載命盤', py: 'jiāzǎi mìngpán' },
  loading_profiles: { en: 'Loading profiles...', id: 'Memuat profil...', zh: '加載檔案', py: 'jiāzǎi dàng\'àn' },
  no_data:        { en: 'No data',          id: 'Tidak ada data',       zh: '無數據', py: 'wú shùjù' },
  saving:         { en: 'Saving...',        id: 'Menyimpan...',         zh: '保存中', py: 'bǎocún zhōng' },
} as const;

// ──────────────────────────────────────────────
// PAGE: HOME
// ──────────────────────────────────────────────

export const HOME = {
  profiles:        { en: 'Profiles',       id: 'Profil',           zh: '檔案', py: 'dàng\'àn' },
  new_profile:     { en: '+ New Profile',  id: '+ Profil Baru',   zh: '+ 新檔案', py: 'xīn dàng\'àn' },
  confirm_delete:  { en: 'Are you sure you want to delete this profile?', id: 'Yakin ingin menghapus profil ini?', zh: '確定要刪除此檔案嗎？', py: 'quèdìng yào shānchú cǐ dàng\'àn ma' },
  failed_load:     { en: 'Failed to load profiles', id: 'Gagal memuat profil', zh: '加載檔案失敗', py: 'jiāzǎi dàng\'àn shībài' },
  failed_delete:   { en: 'Failed to delete profile', id: 'Gagal menghapus profil', zh: '刪除檔案失敗', py: 'shānchú dàng\'àn shībài' },
} as const;

// ──────────────────────────────────────────────
// FORM: PROFILE
// ──────────────────────────────────────────────

export const PROFILE_FORM = {
  create_title:   { en: 'Create New Profile', id: 'Buat Profil Baru',    zh: '創建新檔案', py: 'chuàngjiàn xīn dàng\'àn' },
  name:           { en: 'Name',               id: 'Nama',                zh: '姓名', py: 'xìngmíng' },
  birth_date:     { en: 'Birth Date',         id: 'Tanggal Lahir',       zh: '出生日期', py: 'chūshēng rìqī' },
  birth_time:     { en: 'Birth Time',         id: 'Waktu Lahir',         zh: '出生時間', py: 'chūshēng shíjiān' },
  gender:         { en: 'Gender',             id: 'Jenis Kelamin',       zh: '性別', py: 'xìngbié' },
  male:           { en: 'Male',               id: 'Laki-laki',           zh: '男', py: 'nán' },
  female:         { en: 'Female',             id: 'Perempuan',           zh: '女', py: 'nǚ' },
  whatsapp:       { en: 'WhatsApp',           id: 'WhatsApp',            zh: 'WhatsApp', py: '' },
  optional:       { en: '(optional)',         id: '(opsional)',          zh: '（選填）', py: 'xuǎntián' },
  enter_name:     { en: 'Enter name',         id: 'Masukkan nama',       zh: '輸入姓名', py: 'shūrù xìngmíng' },
  invalid_date:   { en: 'Invalid date',       id: 'Tanggal tidak valid', zh: '日期無效', py: 'rìqī wúxiào' },
  press_m_or_f:   { en: 'Press M or F to select', id: 'Tekan M atau F',  zh: '按 M 或 F 選擇', py: 'àn M huò F xuǎnzé' },
  failed_create:  { en: 'Failed to create profile', id: 'Gagal membuat profil', zh: '創建檔案失敗', py: 'chuàngjiàn dàng\'àn shībài' },
  place_of_birth: { en: 'Place of birth',     id: 'Tempat lahir',        zh: '出生地', py: 'chūshēng dì' },
  phone:          { en: 'Phone',              id: 'Telepon',             zh: '電話', py: 'diànhuà' },
  add_time:       { en: 'Add time...',        id: 'Tambah waktu...',     zh: '添加時間...', py: 'tiānjiā shíjiān' },
  click_to_add:   { en: 'Click to add...',    id: 'Klik untuk tambah...', zh: '點擊添加...', py: 'diǎnjī tiānjiā' },
  click_to_edit:  { en: 'Click to edit',      id: 'Klik untuk edit',     zh: '點擊編輯', py: 'diǎnjī biānjí' },
} as const;

// ──────────────────────────────────────────────
// FORM: LIFE EVENT
// ──────────────────────────────────────────────

export const EVENT_FORM = {
  add_title:        { en: 'Add Life Event',                   id: 'Tambah Peristiwa',                zh: '添加人生事件', py: 'tiānjiā rénshēng shìjiàn' },
  add_button:       { en: 'Add Life Event',                   id: 'Tambah Peristiwa',                zh: '添加人生事件', py: 'tiānjiā rénshēng shìjiàn' },
  date:             { en: 'Date',                             id: 'Tanggal',                         zh: '日期', py: 'rìqī' },
  year_required:    { en: 'Year required, month and day optional', id: 'Tahun wajib, bulan dan hari opsional', zh: '年份必填，月和日選填', py: 'niánfèn bìtián, yuè hé rì xuǎntián' },
  location:         { en: 'Location',                         id: 'Lokasi',                          zh: '地點', py: 'dìdiǎn' },
  where_happened:   { en: 'Where did this happen?',           id: 'Di mana ini terjadi?',            zh: '這件事發生在哪裡？', py: 'zhè jiàn shì fāshēng zài nǎlǐ' },
  notes:            { en: 'Notes',                            id: 'Catatan',                         zh: '備註', py: 'bèizhù' },
  what_happened:    { en: 'What happened during this period?', id: 'Apa yang terjadi pada periode ini?', zh: '這段時期發生了什麼？', py: 'zhè duàn shíqī fāshēng le shénme' },
  duplicate:        { en: 'This date already exists in your life events', id: 'Tanggal ini sudah ada', zh: '此日期已存在', py: 'cǐ rìqī yǐ cúnzài' },
  valid_year:       { en: 'Please enter a valid year (1900-2100)', id: 'Masukkan tahun yang valid (1900-2100)', zh: '請輸入有效年份 (1900-2100)', py: 'qǐng shūrù yǒuxiào niánfèn' },
  specify_month:    { en: 'Please specify a month when adding a day', id: 'Harap tentukan bulan saat menambah hari', zh: '添加日時請先填寫月份', py: 'tiānjiā rì shí qǐng xiān tiánxiě yuèfèn' },
  failed_create:    { en: 'Failed to create life event',      id: 'Gagal membuat peristiwa',          zh: '創建事件失敗', py: 'chuàngjiàn shìjiàn shībài' },
} as const;

// ──────────────────────────────────────────────
// CHART / ANALYSIS
// ──────────────────────────────────────────────

export const CHART = {
  birth_chart:        { en: 'Birth Chart',              id: 'Grafik Kelahiran',        zh: '命盤', py: 'mìngpán' },
  birth:              { en: 'Birth',                    id: 'Kelahiran',               zh: '出生', py: 'chūshēng' },
  ten_year:           { en: '10Y',                      id: '10Th',                    zh: '大運', py: 'dà yùn' },
  interaction_analysis: { en: 'Interaction Analysis (Advanced)', id: 'Analisis Interaksi (Lanjutan)', zh: '交互分析（進階）', py: 'jiāohù fēnxī (jìnjiē)' },
  indicators:         { en: 'Indicators',               id: 'Indikator',               zh: '指標', py: 'zhǐbiāo' },
  guidance:           { en: 'Guidance',                  id: 'Panduan',                 zh: '指導', py: 'zhǐdǎo' },
  add_notes:          { en: 'Add notes about this period...', id: 'Tambahkan catatan tentang periode ini...', zh: '添加此時期的備註...', py: 'tiānjiā cǐ shíqī de bèizhù' },
  click_add_notes:    { en: 'Click to add notes...',    id: 'Klik untuk menambah catatan...', zh: '點擊添加備註...', py: 'diǎnjī tiānjiā bèizhù' },
  post_interaction:   { en: 'Post-interaction',         id: 'Pasca-interaksi',         zh: '交互後', py: 'jiāohù hòu' },
  natal:              { en: 'Natal',                    id: 'Natal',                   zh: '命盤', py: 'mìngpán' },
  esc_cancel:         { en: 'Press Escape to cancel, Cmd+Enter to save', id: 'Tekan Escape untuk batal, Cmd+Enter untuk simpan', zh: '按 Escape 取消，Cmd+Enter 保存', py: 'àn Escape qǔxiāo, Cmd+Enter bǎocún' },
  school:             { en: 'School',                   id: 'Aliran',                  zh: '流派', py: 'liúpài' },
  what_changed:       { en: 'What Changed (vs Natal)',  id: 'Apa yang Berubah (vs Natal)', zh: '變化對比（vs 命盤）', py: 'biànhuà duìbǐ' },
  natal_analysis:     { en: 'Natal Analysis (Birth Chart)', id: 'Analisis Natal (Grafik Kelahiran)', zh: '命盤分析（出生盤）', py: 'mìngpán fēnxī (chūshēng pán)' },
  no_section_data:    { en: 'No data for this section.', id: 'Tidak ada data untuk bagian ini.', zh: '此部分無數據。', py: 'cǐ bùfèn wú shùjù' },
  interactions_count: { en: 'interactions (chronological)', id: 'interaksi (kronologis)', zh: '個交互（時序）', py: 'gè jiāohù (shíxù)' },
} as const;

// ──────────────────────────────────────────────
// ELEMENT ANALYSIS (WU XING)
// ──────────────────────────────────────────────

export const WUXING = {
  title:    { en: 'WU XING',  id: 'WU XING',  zh: '五行', py: 'wǔxíng' },
} as const;

// ──────────────────────────────────────────────
// WEALTH STORAGE
// ──────────────────────────────────────────────

export const WEALTH = {
  title:      { en: 'WEALTH STORAGE', id: 'GUDANG KEKAYAAN', zh: '財庫', py: 'cáikù' },
  no_storage: { en: 'No storage in chart', id: 'Tidak ada gudang di grafik', zh: '命盤中無庫', py: 'mìngpán zhōng wú kù' },
} as const;

// ──────────────────────────────────────────────
// SPIRITUAL SENSITIVITY
// ──────────────────────────────────────────────

export const SPIRITUAL = {
  title: { en: 'SPIRITUAL SENSITIVITY', id: 'SENSITIVITAS SPIRITUAL', zh: '靈性敏感度', py: 'língxìng mǐngǎn dù' },
} as const;

// ──────────────────────────────────────────────
// SEARCH / PROFILE LIST
// ──────────────────────────────────────────────

export const SEARCH = {
  type_to_search:  { en: 'Type to search...',  id: 'Ketik untuk mencari...', zh: '輸入搜索...', py: 'shūrù sōusuǒ' },
  profiles:        { en: 'profiles',            id: 'profil',                 zh: '個檔案', py: 'gè dàng\'àn' },
  navigate:        { en: 'Navigate',            id: 'Navigasi',              zh: '導航', py: 'dǎoháng' },
  open:            { en: 'Open',                id: 'Buka',                  zh: '打開', py: 'dǎkāi' },
  clear:           { en: 'Clear',               id: 'Bersihkan',             zh: '清除', py: 'qīngchú' },
  no_match:        { en: 'No profiles matching', id: 'Tidak ada profil cocok', zh: '沒有匹配的檔案', py: 'méiyǒu pǐpèi de dàng\'àn' },
  no_profiles:     { en: 'No profiles yet',     id: 'Belum ada profil',       zh: '暫無檔案', py: 'zàn wú dàng\'àn' },
  showing:         { en: 'Showing',             id: 'Menampilkan',            zh: '顯示', py: 'xiǎnshì' },
  of:              { en: 'of',                  id: 'dari',                   zh: '/',    py: '' },
  load_more:       { en: '[Load More]',         id: '[Muat Lagi]',            zh: '【加載更多】', py: 'jiāzǎi gèngduō' },
  delete_profile:  { en: 'Delete profile',      id: 'Hapus profil',           zh: '刪除檔案', py: 'shānchú dàng\'àn' },
} as const;

// ──────────────────────────────────────────────
// CALENDAR (DONG GONG)
// ──────────────────────────────────────────────

export const CALENDAR = {
  title:       { en: 'Dong Gong Calendar', id: 'Kalender Dong Gong',  zh: '董公日曆', py: 'dǒnggōng rìlì' },
  today:       { en: 'Today',              id: 'Hari Ini',            zh: '今天', py: 'jīntiān' },
  prev_month:  { en: 'Previous month',     id: 'Bulan sebelumnya',    zh: '上月', py: 'shàng yuè' },
  next_month:  { en: 'Next month',         id: 'Bulan berikutnya',    zh: '下月', py: 'xià yuè' },
  good_for:    { en: 'Good for',           id: 'Baik untuk',          zh: '宜', py: 'yí' },
  avoid:       { en: 'Avoid',              id: 'Hindari',             zh: '忌', py: 'jì' },
  forbidden:   { en: 'Forbidden hours',    id: 'Jam terlarang',       zh: '禁時', py: 'jìn shí' },
  originally:  { en: 'Originally',         id: 'Awalnya',             zh: '原本', py: 'yuánběn' },
  before:      { en: 'Before',             id: 'Sebelum',             zh: '之前', py: 'zhīqián' },
} as const;

export const WEEKDAYS_TRI = [
  { en: 'SU', id: 'MI', zh: '日', py: 'rì' },
  { en: 'MO', id: 'SE', zh: '一', py: 'yī' },
  { en: 'TU', id: 'SE', zh: '二', py: 'èr' },
  { en: 'WE', id: 'RA', zh: '三', py: 'sān' },
  { en: 'TH', id: 'KA', zh: '四', py: 'sì' },
  { en: 'FR', id: 'JU', zh: '五', py: 'wǔ' },
  { en: 'SA', id: 'SA', zh: '六', py: 'liù' },
] as const;

export const MONTHS_TRI = [
  { en: 'January',   id: 'Januari',   zh: '一月',   py: 'yī yuè' },
  { en: 'February',  id: 'Februari',  zh: '二月',   py: 'èr yuè' },
  { en: 'March',     id: 'Maret',     zh: '三月',   py: 'sān yuè' },
  { en: 'April',     id: 'April',     zh: '四月',   py: 'sì yuè' },
  { en: 'May',       id: 'Mei',       zh: '五月',   py: 'wǔ yuè' },
  { en: 'June',      id: 'Juni',      zh: '六月',   py: 'liù yuè' },
  { en: 'July',      id: 'Juli',      zh: '七月',   py: 'qī yuè' },
  { en: 'August',    id: 'Agustus',   zh: '八月',   py: 'bā yuè' },
  { en: 'September', id: 'September', zh: '九月',   py: 'jiǔ yuè' },
  { en: 'October',   id: 'Oktober',   zh: '十月',   py: 'shí yuè' },
  { en: 'November',  id: 'November',  zh: '十一月', py: 'shíyī yuè' },
  { en: 'December',  id: 'Desember',  zh: '十二月', py: 'shí\'èr yuè' },
] as const;

// ──────────────────────────────────────────────
// PASSWORD GATE
// ──────────────────────────────────────────────

export const AUTH = {
  enter_password: { en: 'Enter password to continue', id: 'Masukkan kata sandi untuk melanjutkan', zh: '請輸入密碼繼續', py: 'qǐng shūrù mìmǎ jìxù' },
  password:       { en: 'Password',                    id: 'Kata Sandi',                           zh: '密碼', py: 'mìmǎ' },
  incorrect:      { en: 'Incorrect password',          id: 'Kata sandi salah',                     zh: '密碼錯誤', py: 'mìmǎ cuòwù' },
} as const;

// ──────────────────────────────────────────────
// PROFILE PAGE
// ──────────────────────────────────────────────

export const PROFILE_PAGE = {
  loading:     { en: 'Loading profile...', id: 'Memuat profil...',       zh: '加載檔案中', py: 'jiāzǎi dàng\'àn zhōng' },
  back:        { en: 'Back to Profiles',   id: 'Kembali ke Profil',     zh: '返回檔案列表', py: 'fǎnhuí dàng\'àn lièbiǎo' },
  not_found:   { en: 'Profile not found',  id: 'Profil tidak ditemukan', zh: '找不到檔案', py: 'zhǎo bù dào dàng\'àn' },
} as const;
