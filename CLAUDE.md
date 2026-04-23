# CoffeChat - Flutter App Development Project

## 5-Phase Development Harness

이 프로젝트는 Claude Code 기반 5단계 Flutter 앱 개발 하네스를 사용합니다.

### 사용법

```
/harness <기능 설명>        # 새 세션으로 5단계 개발 시작
/harness --resume           # 중단된 세션 이어서 진행
/harness --phase N          # 특정 Phase부터 시작
/harness --stop             # 현재 세션 중단 (나중에 resume 가능)
/harness --status           # 진행 상태 확인
/harness --list             # 전체 세션 목록
```

### 5 Phases

| Phase | 이름 | 권한 | 설명 |
|-------|------|------|------|
| 1 | Clarify | Read-only | 요구사항 확인, UX/DB/아키텍처 논의 |
| 2 | Context | Read-only | 코드베이스 탐색 (없으면 스킵) |
| 3 | Plan | Read+Write | TASK 분해, 구현 계획 작성 |
| 4 | Execute | Full | 코드 구현 + `dart analyze` 검증 |
| 5 | Evaluate | Read+Bash | 독립 검증 (새 세션, 격리 실행) |

### 핵심 원칙
- Phase별 최소 권한 (Clarify/Context는 Read-only)
- Phase 5는 새 세션으로 격리하여 독립 검증
- Execute/Evaluate 실패 시 Plan으로 자동 루프백 (최대 3회)
- 세션 상태는 `specs/sessions/<id>/state.json`에 원자적 저장

### 디렉토리 구조

```
.claude_harness/
├── scripts/run_phases.py     # Python CLI 오케스트레이터
├── phases/                   # Phase별 프롬프트
│   ├── 01_clarify.md
│   ├── 02_context.md
│   ├── 03_plan.md
│   ├── 04_execute.md
│   └── 05_evaluate.md
└── sessions/                 # Python 스크립트용 세션 (CLI 외부 자동화)

specs/
├── sessions/                 # /harness 커맨드 세션 산출물
│   └── <session_id>/
│       ├── state.json
│       └── 01~05_*.md
└── latest.txt                # 최근 세션 ID

docs/
├── SERVICE_BLUEPRINT.md      # 서비스 블루프린트 (서비스 정의, 사용자 여정)
├── harness.md                # 하네스 설계 문서
├── TASK_TEMPLATE.md          # TASK 파일 양식
└── design/
    ├── DESIGN_SYSTEM.md      # 디자인 시스템 마스터 문서
    └── design_tokens.json    # 코드용 디자인 토큰
```

### 서비스 블루프린트 참조 규칙
- `docs/SERVICE_BLUEPRINT.md`에 서비스 정의, 핵심 가치, 사용자 여정 등이 정의되어 있음
- Phase 1 (Clarify)에서 **반드시** 이 문서를 먼저 읽고 서비스 맥락을 파악한 후 요구사항 분석
- 기능 개발 중 서비스 방향성/범위 판단이 필요할 때 이 문서를 참조

### 디자인 참조 규칙 (필수)
- 프론트엔드(화면/위젯) 구축 또는 수정 시 **반드시** 아래 2개 파일을 참조할 것:
  - `docs/design/DESIGN_SYSTEM.md` — 디자인 시스템 마스터 문서 (색상, 타이포, 간격, 컴포넌트, 상태별 UI)
  - `docs/design/design_tokens.json` — 코드에서 직접 사용하는 디자인 토큰 값
- DESIGN_SYSTEM.md를 수정하면 design_tokens.json도 반드시 동기화
- Plan Phase에서 각 프론트엔드 Task에 `참조 디자인:` 필드 필수 기재

### Flutter 코딩 컨벤션
- SDK: Dart ^3.8.1
- 아키텍처: Clean Architecture (domain / data / presentation)
- 파일명: `snake_case.dart`
- 클래스명: `PascalCase`
- `const` 적극 활용, `dynamic` 사용 금지
- `print()` 금지 → `dart:developer log()` 사용
- `.freezed.dart`, `.g.dart` 코드 생성 파일 필요시 `build_runner` 실행
