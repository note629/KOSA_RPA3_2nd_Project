window.onload = function () {
  var dropzone = document.getElementById("dropzone");
  var fileInput = document.getElementById("id_input_img");

  dropzone.ondragover = function () {
    this.className = "dragover";
    return false;
  };

  dropzone.ondragleave = function () {
    this.className = "";
    return false;
  };

  dropzone.ondrop = function (e) {
    e.preventDefault();
    this.className = "";

    fileInput.files = e.dataTransfer.files;

    var event = new Event("change");
    fileInput.dispatchEvent(event);
  };

  // 파일 input의 change 이벤트 핸들러 추가
  fileInput.addEventListener("change", function (e) {
    if (this.files && this.files[0]) {
      // 파일이 선택되었는지 확인
      var reader = new FileReader();
      reader.onloadend = function (e) {
        dropzone.style.backgroundImage = "url(" + e.target.result + ")"; // 읽어들인 결과(이미지 데이터 URL)를 배경 이미지로 설정
        dropzone.style.backgroundSize = "contain"; // 배경 이미지 크기 조절
        dropzone.style.backgroundPosition = "center"; // 배경 이미지 위치 조절
        dropzone.style.backgroundRepeat = "no-repeat"; // 배경 이미지 반복 방식 설정

        dropzone.textContent = ""; // 텍스트 내용 제거
      };
      reader.readAsDataURL(this.files[0]); // 파일을 읽어들임
    } else {
      dropzone.style.backgroundImage = ""; // 선택된 파일이 없으면 배경 이미지 초기화

      dropzone.textContent = "Drag & Drop"; // 원래의 텍스트로 복원
    }
  });
};
