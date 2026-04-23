# CoffeChat — Flutter App Harness

Claude Code 기반 5단계 Flutter 앱 개발 하네스.

## 개요

Phase별 최소 권한 원칙을 적용하고, 실행 단계에서 병렬 서브에이전트로 TASK를 동시 구현합니다.

## 5 Phases

| Phase | 이름 | 권한 | 설명 |
|-------|------|------|------|
| 1 | **Clarify** | Read-only | 요구사항 확인, UX/DB/아키텍처 논의 |
| 2 | **Context** | Read-only | 코드베이스 탐색 (없으면 스킵) |
| 3 | **Plan** | Read+Write | TASK 분해, 병렬 실행 그룹 계획 |
| 4 | **Execute** | Full | 병렬 서브에이전트 코드 구현 + `dart analyze` 검증 |
| 5 | **Evaluate** | Read+Bash | 독립 검증 (AC 기반, 격리 실행) |

## 사용법

Claude Code에서:

```
/harness <기능 설명>        # 새 세션으로 5단계 개발 시작
/harness --resume           # 중단된 세션 이어서 진행
/harness --phase N          # 특정 Phase부터 시작
/harness --stop             # 현재 세션 중단
/harness --status           # 진행 상태 확인
/harness --list             # 전체 세션 목록
```

CLI 외부 자동화:

```bash
python .claude_harness/scripts/run_phases.py new "채팅 타이머 기능"
python .claude_harness/scripts/run_phases.py status
python .claude_harness/scripts/run_phases.py list
```

## Phase 4 — 병렬 실행 모델

```
┌─ Group 1 (병렬) ──────────────────────┐
│  Agent 1: TASK-001 (executor/sonnet)  │
│  Agent 2: TASK-002 (designer/sonnet)  │
└──────────────┬────────────────────────┘
               ▼ dart analyze 검증
┌─ Group 2 (병렬) ──────────────────────┐
│  Agent 3: TASK-003 (executor/sonnet)  │
│  Agent 4: TASK-004 (executor-low)     │
└──────────────┬────────────────────────┘
               ▼ 전체 통합 검증
```

- 파일 소유권이 겹치지 않는 TASK끼리 병렬 실행
- TASK 유형에 따라 에이전트 자동 배정
- Execute/Evaluate 실패 시 Plan으로 루프백 (최대 3회)

## 디렉토리 구조

```
.claude_harness/
├── phases/               # Phase별 프롬프트 (01~05)
├── scripts/              # Python CLI 오케스트레이터
└── sessions/             # CLI 외부 자동화용 세션

.claude/commands/
└── harness.md            # /harness 스킬 정의

specs/
├── sessions/             # 세션별 산출물 (state.json, 01~05_*.md)
└── latest.txt            # 최근 세션 ID

docs/
├── SERVICE_BLUEPRINT.md  # 서비스 블루프린트
├── harness.md            # 하네스 설계 문서
├── TASK_TEMPLATE.md      # TASK 파일 양식
└── design/
    ├── DESIGN_SYSTEM.md  # 디자인 시스템
    └── design_tokens.json
```

## Flutter 코딩 컨벤션

- SDK: Dart ^3.8.1
- 아키텍처: Clean Architecture (domain / data / presentation)
- 파일명: `snake_case.dart` / 클래스명: `PascalCase`
- `const` 적극 활용, `dynamic` 사용 금지
- `print()` 금지 → `dart:developer log()` 사용
