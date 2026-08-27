# Spectre

## Tóm tắt

File đề bài là một ảnh phổ âm thanh không còn thông tin pha. Ta đổi giá trị xám trở lại mel power spectrogram, dùng Griffin–Lim ước lượng pha, rồi phát WAV thu được. Giọng nói đọc lần lượt từng ký tự của flag.

Flag đã xác minh:

```text
L3AK{5p3c7r3_0f_7h3_fr3qu3ncy_r34lm_r3m41n5_w17h1n_7h3_5p3c7r0gr4m_l34v1ng_gh057ly_7r4c35_0f_wh47_0nc3_w45}
```

## Đề bài yêu cầu gì?

Đề nói sẽ “say it out loud” và cho biết charset của flag. Attachment duy nhất là `spectre.png`, một PNG grayscale rất dài. Mục tiêu là biến biểu diễn phổ này trở lại thành âm thanh đủ rõ để nghe chuỗi ký tự.

## Kiến thức nền

Spectrogram biểu diễn năng lượng của âm thanh theo hai trục:

- trục ngang là thời gian;
- trục dọc là tần số;
- độ sáng là năng lượng.

Mel spectrogram dùng thang mel để phân bố các dải tần gần với cảm nhận của tai người. Ảnh chỉ lưu độ lớn/năng lượng, không lưu **pha** của các thành phần Fourier. Vì vậy không thể gọi inverse FFT trực tiếp để lấy đúng tín hiệu ban đầu.

Griffin–Lim giải vấn đề này bằng cách khởi tạo pha, chuyển qua lại giữa miền thời gian và miền tần số, rồi lặp để phổ của tín hiệu tái dựng ngày càng gần phổ đầu vào. Âm thanh không hoàn hảo nhưng thường đủ cho giọng nói.

## Phân tích ban đầu

Các thuộc tính quan trọng:

```text
SHA-256: e85821313acfb8f480eba24472917c670bbc0fb27d3d4356cf1705c59d8acbbf
mode: L (grayscale)
size: 4494 x 192
metadata: không có
```

Chiều cao đúng 192 và hình dạng các dải năng lượng gợi ý 192 mel bins. Khi lấy percentile 90 theo từng cột và threshold từ 8 đến 64, kết quả luôn là đúng 107 cụm hoạt động. Mỗi cụm tương ứng khoảng một ký tự được đọc, xen giữa là khoảng im lặng.

## Vì sao chọn nghịch đảo mel spectrogram?

Giả thuyết STFT tuyến tính đầu tiên dùng `192 = n_fft/2 + 1`, tức `n_fft=382`. Hai hướng trục tần số đều tạo WAV khoảng 19,56 giây nhưng ASR chỉ trả nhiễu với confidence gần 0. Đây là tín hiệu bác bỏ cấu hình tuyến tính.

Với mel spectrogram và cấu hình phổ biến `n_fft=2048`, `hop_length=512`, 4494 frame tạo WAV khoảng 104,33 giây. Thời lượng này khớp 107 cụm, gần một giây cho mỗi ký tự; ASR cũng bắt đầu đọc được wrapper, chữ cái, chữ số và từ “underscore”.

## Cách giải tối thiểu

Cài dependency vào môi trường tạm:

```powershell
python -m pip install -r .\solve\requirements.txt
```

Chạy solver từ thư mục challenge:

```powershell
python .\solve\reconstruct.py .\files\spectre.png -o recovered.wav --seed 0
```

Kết quả cần có:

```text
spoken_units=107
duration_seconds=104.327256
```

Mở `recovered.wav` và ghi lại từng ký tự. Các chữ số leetspeak được đọc riêng, ví dụ `3` là “three”, `7` là “seven”; từ “underscore” phải chuyển thành `_`. Câu sau khi ghép và giữ nguyên chữ số là flag ở phần tóm tắt.

## Xác minh flag

Không dùng một transcript ASR duy nhất làm bằng chứng. Việc xác minh gồm:

1. Cả một dải threshold đều tách đúng 107 cụm; flag ghép được cũng dài đúng 107 ký tự.
2. Chạy Griffin–Lim với `random_state=0` và `random_state=1` đều cho 2.300.416 sample, tương đương 104,327256 giây.
3. Whisper `tiny.en` và `base.en` được chạy trên các cửa sổ 12 cụm, chồng lấn 2 cụm. Hai model và hai seed cùng nhận ra các đoạn dài như `r34lm_r3m41n5`, `5p3c7r0gr4m`, `l34v1ng_gh057ly`, `7r4c35_0f_wh47_0nc3_w45`.
4. Chuỗi cuối có wrapper/charset đúng đề và giải leetspeak thành câu tiếng Anh hoàn chỉnh: “spectre of the frequency realm remains within the spectrogram leaving ghostly traces of what once was”.

Evidence gọn nằm trong `solve/evidence/reconstruction.txt`.

## Những hướng thử không hiệu quả

- Coi 192 hàng là STFT tuyến tính và suy ra `n_fft=382`: WAV quá ngắn, ASR gần như chỉ thấy nhiễu.
- Đảo hướng tần số nhưng giữ mô hình STFT tuyến tính: không cải thiện.
- Dùng Windows Speech Recognizer trên toàn WAV: engine cũ có confidence rất thấp.
- Nhận dạng từng token một: mất ngữ cảnh nên cả Windows ASR và Whisper nhầm nhiều chữ cái. Cửa sổ chồng lấn 10–12 token hiệu quả hơn.
- Gom cụm bằng nearest-neighbor trên ảnh: chỉ đạt 42,4% vì giọng nói có coarticulation và cùng một ký tự không tạo patch giống hệt nhau.

## Bài học và lỗi thường gặp

- Kích thước một ảnh phổ là manh mối về loại phổ và tham số biến đổi, nhưng phải kiểm chứng bằng thời lượng/tín hiệu thu được.
- Ảnh spectrogram thường đặt tần số cao ở trên; ma trận mel của librosa lại xếp thấp đến cao, nên cần `flipud`.
- Pixel thường biểu diễn dB chứ không phải biên độ tuyến tính. Ở đây cần đổi miền `[-80, 0] dB` về power trước khi nghịch đảo.
- Griffin–Lim có pha khởi tạo ngẫu nhiên. Dùng seed cố định để tái lập và đổi seed khi xác minh.
- ASR dễ nhầm tên chữ cái và chữ số (`3/E`, `7/T`). Hãy dùng cửa sổ chồng lấn, kiểm tra số cụm, charset và nghĩa của toàn câu; không chép mù một transcript.

## Nguồn tham khảo

- [librosa.feature.inverse.mel_to_audio](https://librosa.org/doc/0.11.0/generated/librosa.feature.inverse.mel_to_audio.html): API chính thức để nghịch đảo mel power spectrogram bằng Griffin–Lim.
- [librosa.griffinlim](https://librosa.org/doc/0.11.0/generated/librosa.griffinlim.html): tham số, giả định và cơ chế ước lượng pha.
- [OpenAI Whisper](https://github.com/openai/whisper): mô hình ASR và hướng dẫn transcription.
- [Whisper tiny.en model card](https://huggingface.co/openai/whisper-tiny.en): checkpoint tiếng Anh dùng để đối chiếu transcript.
