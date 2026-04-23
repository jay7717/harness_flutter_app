# Phase 3: Plan (Read + Write)

## 목적
TASK를 분해하고 구현 계획을 작성한다.

## 권한
- **Read + Write**: 문서 읽기/쓰기 허용
- 코드 파일(`.dart`) 생성/수정 금지

## 수행 절차

### 1. TASK 분해
Phase 1의 AC와 Phase 2의 컨텍스트를 기반으로:
- 독립적으로 실행 가능한 TASK 단위로 분해
- `docs/TASK_TEMPLATE.md` 양식 준수
- 각 TASK에 ID, 우선순위, 예상 공수, 의존관계 부여

### 2. 병렬화 계획
- **의존관계가 없는 TASK는 `Parallelizable: Yes`로 표기**
- 병렬 실행 그룹 정의 (Group A: TASK-001,002 / Group B: TASK-003 ...)
- 각 그룹 내 TASK는 서로 다른 파일을 대상으로 해야 함 (충돌 방지)

### 3. 프론트엔드 TASK 디자인 참조
- 화면/위젯 관련 TASK에는 `참조 디자인:` 필드 필수 기재
- `docs/design/DESIGN_SYSTEM.md`의 해당 섹션 명시

### 4. 실행 순서 결정
```
Group 1 (병렬) → Group 2 (병렬) → Group 3 (병렬) → ...
```
- 그룹 간에는 순차 실행 (의존관계)
- 그룹 내에서는 병렬 실행 (독립 TASK)

### 5. 사용자 확인
- TASK 목록과 실행 계획을 사용자에게 보여주고 승인 요청
- **사용자 승인 없이 Phase 4로 넘어가지 않는다**

## 산출물

### `specs/sessions/<session_id>/03_plan.md`
```markdown
# Implementation Plan

## TASK 목록
| ID | 제목 | 우선순위 | 공수 | 의존 | 병렬 | 그룹 |
|----|------|----------|------|------|------|------|
| TASK-001 | ... | P0 | ~1h | 없음 | Yes | G1 |
| TASK-002 | ... | P0 | ~1h | 없음 | Yes | G1 |
| TASK-003 | ... | P1 | ~2h | 001 | Yes | G2 |

## 실행 그룹
### Group 1 (병렬)
- TASK-001: ...
- TASK-002: ...

### Group 2 (병렬, Group 1 완료 후)
- TASK-003: ...
- TASK-004: ...

## 파일 소유권 (충돌 방지)
| TASK | 생성/수정 파일 |
|------|---------------|
| TASK-001 | lib/features/x/domain/... |
| TASK-002 | lib/features/x/data/... |
```

### `specs/sessions/<session_id>/TASK-XXX.md` (각 TASK별)
- `docs/TASK_TEMPLATE.md` 양식에 따라 작성

## 완료 조건
- 모든 TASK 분해 완료
- 병렬 실행 그룹 정의 완료
- 파일 소유권 충돌 없음 확인
- 사용자 승인 완료
