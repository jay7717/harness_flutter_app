# TASK-XXX: <제목> [P]

**ID**: TASK-XXX
**Effort**: ~Nh
**Dependencies**: TASK-YYY (없으면 "없음")
**Parallelizable**: Yes | No

## 목적
이 태스크가 왜 필요한지 1-2문장으로 설명.

## 작업 내용

### 1. <사용자 스토리>
사용자가 어떤 목적을 갖고 이 기능을 사용하는지 작성.

<샘플>
예1: 사용자는 특정 날짜에 어디에 얼마를 지출했는지 간단하게 기록하고 싶다.
예2: 사용자는 궁금한 것을 해결하기 위해 커피챗 진행 시 남은 시간을 실시간으로 확인하고 싶다.

### 2. <정책>
기능 단위로 상태, 액션 결과, 기본값, 초기값 등을 개조식으로 간단하게 정의.

### 3. <유즈케이스>
기능 별로 성공/실패 부분 정의.

<샘플>
유즈케이스-예1 UC-1 수입/지출 내역 작성 (Create)
1. [사용자] 거래타입(지출)을 선택한다.
2. [사용자] 날짜, 금액, 카테고리, 메모(선택)를 입력한다.
3. [사용자] '저장하기' 버튼을 누른다.
4. [시스템] 필수 입력값(카테고리, 금액)이 유효한지 검증한다.
5. [시스템] 데이터를 저장하고, 홈 화면으로 이동시킨다.

### 4. <작업 항목>
구체적인 구현 내용. 필요시 코드 스니펫 포함.

```dart
// 예시 코드
```

### 5. <작업 항목>
...

## 생성/수정 파일
- CREATE: `lib/features/<feature>/<layer>/<file>.dart`
- MODIFY: `lib/core/<file>.dart`
- DELETE: `lib/<old_file>.dart`

## Acceptance Criteria
- [ ] AC-1: 구체적이고 검증 가능한 기준
- [ ] AC-2: ...
- [ ] `flutter analyze` 에러 0개
- [ ] `flutter pub get` 성공

## 매핑된 AC
- clarify_summary.md의 AC 번호와 매핑 (예: AC 1-1, AC 3-2)

## Test Plan
- **Unit**: 테스트 대상 및 방법
- **Widget**: N/A 또는 테스트 설명
- **Integration**: deferred to TASK-XXX 또는 테스트 설명

## 주의사항
- 구현 시 주의할 점, 엣지케이스, 제약사항 등
- `.freezed.dart`, `.g.dart` 재생성 필요 여부
- `print()` 금지 — `dart:developer log()` 사용
