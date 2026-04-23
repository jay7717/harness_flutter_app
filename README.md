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

## 포크 & 로컬 셋업 가이드

이 하네스를 포크해서 자신의 Flutter 프로젝트에 적용하는 방법입니다.

### 사전 요구사항

- [Claude Code CLI](https://docs.anthropic.com/en/docs/claude-code) 설치 완료
- Git, Flutter SDK, Python 3.10+ 설치
- GitHub 계정

### Step 1. 포크 & 클론

```bash
# 1. GitHub에서 Fork 버튼 클릭 (https://github.com/jay7717/harness_flutter_app)

# 2. 포크한 리포 클론
git clone https://github.com/<your-username>/harness_flutter_app.git
cd harness_flutter_app
```

### Step 2. 프로젝트 커스터마이징

#### 2-1. `CLAUDE.md` 수정 — 프로젝트명 및 컨벤션

파일 상단의 프로젝트명과 코딩 컨벤션을 자신의 프로젝트에 맞게 수정합니다.

```markdown
# <내 프로젝트명> - Flutter App Development Project
```

필요에 따라 아래 항목을 조정:
- Flutter SDK / Dart 버전
- 아키텍처 패턴 (Clean Architecture, MVVM 등)
- 상태 관리 (Riverpod, BLoC 등)
- 추가 코딩 컨벤션

#### 2-2. `docs/SERVICE_BLUEPRINT.md` 수정 — 서비스 정의

자신의 서비스에 맞게 작성합니다:
- 서비스 정의, 핵심 가치
- 타겟 사용자
- 사용자 여정 (User Journey)

#### 2-3. `docs/design/` 수정 — 디자인 시스템

- `DESIGN_SYSTEM.md`: 색상, 타이포그래피, 간격, 컴포넌트 규칙
- `design_tokens.json`: 코드에서 참조할 디자인 토큰 값

### Step 3. Flutter 프로젝트 초기화 (신규인 경우)

```bash
flutter create . --org com.yourcompany --project-name your_app
flutter pub get
```

기존 Flutter 프로젝트에 하네스를 추가하는 경우, `lib/`가 이미 있으면 이 단계는 스킵합니다.

### Step 4. Claude Code에서 실행

```bash
# 프로젝트 디렉토리에서 Claude Code 실행
claude

# 하네스 시작 — 만들고 싶은 기능을 설명
/harness 커피챗 예약 기능 구현
```

Claude Code가 자동으로:
1. **Phase 1**: 요구사항 분석 → 사용자 확인 요청
2. **Phase 2**: 기존 코드 탐색 (신규면 스킵)
3. **Phase 3**: TASK 분해 + 병렬 실행 계획 → 사용자 승인 요청
4. **Phase 4**: 서브에이전트 병렬 구현 + `dart analyze` 검증
5. **Phase 5**: 독립 검증 → PASS/FAIL 판정

### Step 5. 세션 관리

```bash
# Claude Code 내에서:
/harness --status           # 현재 진행 상태 확인
/harness --resume           # 중단된 세션 이어서 진행
/harness --stop             # 세션 중단 (나중에 resume)
/harness --list             # 전체 세션 목록
/harness --phase 4          # 특정 Phase부터 재시작
```

### 커스터마이징 포인트 요약

| 파일 | 수정 내용 | 필수 여부 |
|------|-----------|-----------|
| `CLAUDE.md` | 프로젝트명, SDK 버전, 코딩 컨벤션 | **필수** |
| `docs/SERVICE_BLUEPRINT.md` | 서비스 정의, 사용자 여정 | **필수** |
| `docs/design/DESIGN_SYSTEM.md` | 디자인 시스템 규칙 | 프론트엔드 시 필수 |
| `docs/design/design_tokens.json` | 디자인 토큰 값 | 프론트엔드 시 필수 |
| `docs/TASK_TEMPLATE.md` | TASK 양식 커스터마이징 | 선택 |
| `.claude_harness/phases/*.md` | Phase 프롬프트 커스터마이징 | 선택 |
| `.claude/commands/harness.md` | 스킬 동작 수정 | 선택 |

### 주의사항

- `/harness` 커맨드는 **Claude Code CLI 환경에서만** 동작합니다 (`.claude/commands/`에 등록된 스킬)
- Phase 1, 3에서 **사용자 승인 없이 다음 단계로 넘어가지 않습니다** — 반드시 확인 후 승인
- Phase 4 병렬 실행 시 에이전트 간 **파일 충돌이 없도록** Plan 단계에서 소유권을 배정합니다
- Execute/Evaluate 실패 시 **최대 3회** Plan으로 자동 루프백합니다

## Flutter 코딩 컨벤션

- SDK: Dart ^3.8.1
- 아키텍처: Clean Architecture (domain / data / presentation)
- 파일명: `snake_case.dart` / 클래스명: `PascalCase`
- `const` 적극 활용, `dynamic` 사용 금지
- `print()` 금지 → `dart:developer log()` 사용
