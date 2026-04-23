# Phase 4: Execute (Full 권한)

## 목적
Plan Phase의 TASK를 병렬 서브에이전트로 구현한다.

## 권한
- **Full**: 모든 파일 읽기/쓰기/실행 허용

## 핵심 원칙: 병렬 서브에이전트 실행
- **그룹 내 TASK는 서브에이전트에 위임하여 동시 실행**
- 각 서브에이전트는 자신의 TASK 파일 소유권 범위만 수정
- 오케스트레이터(메인)는 진행 상황 조율만 담당

## 수행 절차

### 1. 사전 준비
- `specs/sessions/<session_id>/03_plan.md` 읽어 실행 그룹 확인
- 각 TASK 파일(`TASK-XXX.md`) 읽어 작업 내용 확인
- `flutter pub get` 실행하여 의존성 확인

### 2. 그룹별 병렬 실행

각 실행 그룹에 대해:

```
┌─ Group N ──────────────────────────────────────┐
│                                                 │
│  ┌─ Agent 1 ─┐  ┌─ Agent 2 ─┐  ┌─ Agent 3 ─┐ │
│  │ TASK-001   │  │ TASK-002   │  │ TASK-003   │ │
│  │ (executor) │  │ (executor) │  │ (designer) │ │
│  └─────┬──────┘  └─────┬──────┘  └─────┬──────┘ │
│        │               │               │        │
│        └───────────┬────┘───────────────┘        │
│                    ▼                             │
│            그룹 완료 검증                          │
└─────────────────────────────────────────────────┘
                     ▼
              다음 그룹 실행
```

#### 에이전트 배정 규칙
| TASK 유형 | 서브에이전트 | 모델 |
|-----------|-------------|------|
| Domain/Data 레이어 | `oh-my-claudecode:executor` | sonnet |
| 단순 모델/설정 | `oh-my-claudecode:executor-low` | haiku |
| 복잡한 리팩토링 | `oh-my-claudecode:executor-high` | opus |
| UI/위젯/화면 | `oh-my-claudecode:designer` | sonnet |
| 복잡한 UI 시스템 | `oh-my-claudecode:designer-high` | opus |

#### 에이전트 프롬프트 템플릿
각 서브에이전트에게 전달할 정보:
1. TASK 파일 전체 내용
2. Phase 2 컨텍스트 (관련 기존 코드)
3. 디자인 토큰 (프론트엔드인 경우)
4. **파일 소유권 범위** — 이 범위 밖 파일 수정 금지

### 3. 그룹 완료 검증
각 그룹 완료 후:
- `dart analyze` 실행 → 에러 0개 확인
- `dart format --set-exit-if-changed .` 실행
- 에러 발생 시 해당 TASK의 에이전트에게 수정 위임

### 4. 전체 통합 검증
모든 그룹 완료 후:
- `flutter pub get` 실행
- `dart analyze` 전체 실행
- `flutter test` (테스트가 있는 경우)
- build_runner 필요 시: `dart run build_runner build --delete-conflicting-outputs`

### 5. 실패 시 루프백
- `dart analyze` 에러가 해결 불가능한 경우 → **Phase 3(Plan)으로 루프백**
- 루프백은 최대 3회까지 허용
- 루프백 시 `state.json`에 `loopback_count` 기록

## 산출물
`specs/sessions/<session_id>/04_execute_report.md`

```markdown
# Execute Report

## 실행 결과
| TASK | 에이전트 | 상태 | 비고 |
|------|---------|------|------|
| TASK-001 | executor (sonnet) | ✅ 완료 | |
| TASK-002 | executor (sonnet) | ✅ 완료 | |
| TASK-003 | designer (sonnet) | ✅ 완료 | |

## 검증 결과
- dart analyze: ✅ 에러 0개
- dart format: ✅
- flutter test: ✅ / N/A
- build_runner: ✅ / N/A

## 생성/수정된 파일
- CREATE: ...
- MODIFY: ...

## 루프백 횟수: 0/3
```

## 완료 조건
- 모든 TASK 구현 완료
- `dart analyze` 에러 0개
- 통합 검증 통과
- `04_execute_report.md` 작성 완료
