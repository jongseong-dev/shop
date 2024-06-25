# 동적으로 PDF 인보이스 생성하기

- 파이썬으로 PDF를 생성하는데 널리 사용되는 라이브러리 중 하나는 `ReportLab`이다.
- 대부분의 경우 PDF 파일에 커스텀 스타일과 서식을 추가해야한다.
- HTML 템플릿에서 PDF파일을 생성하는 작업을 위해서 `WeasyPrint` 라이브러리를 사용해보자

## 트러블 슈팅

### WeasyPrint 설치 시 오류
- OS 환경이 Windows인 경우, WeasyPrint를 설치할 때 오류가 발생할 수 있다.
- 에러메시지는 다음과 같았다
```bash
OSError: cannot load library 'gobject-2.0-0': error 0x7e.  Additionally, ctypes.util.find_library() did not manage to locate a library called 'gobject-2.0-0' 
```
- 해결 방법은 [weasyprint 공식 문서](https://doc.courtbouillon.org/weasyprint/stable/first_steps.html#windows)에서 설치 방법을 참고하자.
- 또한 해당 글을 보고 시스템 환경변수를 추가하였다. https://stackoverflow.com/questions/63449770/oserror-cannot-load-library-gobject-2-0-error-0x7e