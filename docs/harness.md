# 5-Phase Development Harness 설계 문서

## 개요
Claude Code 기반 5단계 Flutter 앱 개발 하네스.
각 Phase는 최소 권한 원칙을 따르며, Phase 4는 병렬 서브에이전트로 실행한다.

## 아키텍처

```
사용자 → /harness <기능>
              │
              ▼
     ┌─ Phase 1: Clarify ─┐  Read-only
     │  요구사항 확인/승인   │
     └────────┬────────────┘
              ▼
     ┌─ Phase 2: Context ─┐  Read-only (스킵 가능)
     │  코드베이스 탐색      │
     └────────┬────────────┘
              ▼
     ┌─ Phase 3: Plan ────┐  Read+Write
     │  TASK 분해/병렬계획  │◄──────────┐
     └────────┬────────────┘           │
              ▼                    루프백 (최대 3회)
     ┌─ Phase 4: Execute ─┐  Full     │
     │  병렬 서브에이전트    │           │
     │  구현 + dart analyze │           │
     └────────┬────────────┘           │
              ▼                        │
     ┌─ Phase 5: Evaluate ┐  Read+Bash│
     │  독립 검증 (격리)    │───FAIL───┘
     └────────┬────────────┘
              ▼
           PASS → 완료
```

## Phase 4 병렬 실행 모델

### 원칙
- Plan Phase에서 정의한 **실행 그룹** 단위로 병렬 실행
- 각 그룹 내 TASK는 **파일 소유권이 겹치지 않아야** 함
- 그룹 간에는 순차 실행 (의존관계 존재)

### 서브에이전트 매핑
| TASK 유형 | 에이전트 | 모델 |
|-----------|---------|------|
| Domain/Data | executor | sonnet |
| 단순 설정 | executor-low | haiku |
| 복잡 리팩토링 | executor-high | opus |
| UI/위젯 | designer | sonnet |
| 복잡 UI | designer-high | opus |

### 충돌 방지
- Plan Phase에서 파일 소유권 테이블 작성
- 같은 파일을 2개 이상의 TASK가 수정하면 같은 그룹에 넣지 않음
- 공유 파일(라우터, exports)은 마지막 그룹에서 단일 TASK로 처리

## 세션 관리

### 상태 파일: `specs/sessions/<id>/state.json`
```json
{
  "session_id": "20260423_143000_feature_name",
  "feature": "기능 설명",
  "current_phase": 1,
  "status": "in_progress",
  "loopback_count": 0,
  "max_loopback": 3,
  "phases": {
    "1": { "status": "completed", "started_at": "...", "completed_at": "..." },
    "2": { "status": "skipped" },
    "3": { "status": "pending" },
    "4": { "status": "pending" },
    "5": { "status": "pending" }
  },
  "created_at": "2026-04-23T14:30:00",
  "updated_at": "2026-04-23T14:30:00"
}
```

### 세션 ID 규칙
`YYYYMMDD_HHMMSS_<feature_slug>` (예: `20260423_143000_chat_timer`)

## 커맨드

| 명령 | 동작 |
|------|------|
| `/harness <기능>` | 새 세션 생성, Phase 1부터 시작 |
| `/harness --resume` | 최근 세션의 중단 지점부터 재개 |
| `/harness --phase N` | 특정 Phase부터 시작 |
| `/harness --stop` | 현재 세션 중단 (나중에 resume) |
| `/harness --status` | 현재 세션 진행 상태 |
| `/harness --list` | 전체 세션 목록 |
