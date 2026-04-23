# Phase 5: Evaluate (Read + Bash)

## 목적
독립적으로 구현 결과를 검증한다. Phase 4와 격리된 시점에서 수행.

## 권한
- **Read + Bash**: 코드 읽기, 명령어 실행만 허용
- 파일 수정 금지

## 핵심 원칙
- Phase 4의 맥락에 의존하지 않고 **독립적으로** 검증
- Clarify의 AC를 기준으로 하나씩 검증

## 수행 절차

### 1. AC 기반 검증
`01_clarify_summary.md`의 Acceptance Criteria를 하나씩 확인:

| AC | 검증 방법 |
|----|-----------|
| 코드 존재 여부 | 파일/클래스/메서드 존재 확인 (Read, Grep) |
| 정적 분석 | `dart analyze` |
| 포맷 | `dart format --set-exit-if-changed .` |
| 테스트 | `flutter test` |
| 빌드 | `flutter build apk --debug` (선택) |
| 코드 품질 | 패턴 준수, 컨벤션 확인 |

### 2. 정적 검증
```bash
flutter pub get
dart analyze
dart format --set-exit-if-changed .
```

### 3. 테스트 실행
```bash
flutter test
```

### 4. 코드 품질 점검
- Clean Architecture 레이어 분리 준수 여부
- `print()` 사용 여부 (금지)
- `dynamic` 사용 여부 (금지)
- `const` 활용 여부
- 파일명 snake_case 준수
- 디자인 토큰 적용 여부 (프론트엔드)

### 5. 결과 판정
- **PASS**: 모든 AC 통과 + 정적 검증 통과
- **FAIL**: 하나라도 실패 → Phase 3(Plan)으로 루프백

## 산출물
`specs/sessions/<session_id>/05_evaluate_report.md`

```markdown
# Evaluate Report

## 판정: PASS / FAIL

## AC 검증 결과
| AC | 내용 | 결과 | 비고 |
|----|------|------|------|
| AC 1-1 | ... | ✅ / ❌ | |
| AC 1-2 | ... | ✅ / ❌ | |

## 정적 검증
- dart analyze: ✅ / ❌ (에러 N개)
- dart format: ✅ / ❌
- flutter test: ✅ / ❌ / N/A

## 코드 품질
- Clean Architecture 준수: ✅ / ❌
- print() 미사용: ✅ / ❌
- dynamic 미사용: ✅ / ❌
- const 활용: ✅ / ❌
- 네이밍 컨벤션: ✅ / ❌
- 디자인 토큰 적용: ✅ / ❌ / N/A

## 실패 항목 상세 (FAIL인 경우)
- ...

## 루프백 권고 (FAIL인 경우)
- 수정 필요 TASK: ...
- 권고 사항: ...
```

## 완료 조건
- 모든 AC 검증 완료
- 판정 결과 기록
- FAIL 시 루프백 권고 포함
