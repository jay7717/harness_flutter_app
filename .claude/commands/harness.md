# /harness — 5-Phase Flutter Development Harness

## 사용법
```
/harness <기능 설명>        # 새 세션으로 5단계 개발 시작
/harness --resume           # 중단된 세션 이어서 진행
/harness --phase N          # 특정 Phase부터 시작
/harness --stop             # 현재 세션 중단
/harness --status           # 진행 상태 확인
/harness --list             # 전체 세션 목록
```

## 인자: $ARGUMENTS

---

## 실행 로직

### 1. 인자 파싱

**`--status`인 경우:**
- `specs/latest.txt`에서 최근 세션 ID 읽기
- `specs/sessions/<id>/state.json` 읽어 상태 출력
- 종료

**`--list`인 경우:**
- `specs/sessions/` 하위 디렉토리 목록 출력
- 각 `state.json`의 feature, status, current_phase 표시
- 종료

**`--stop`인 경우:**
- `specs/latest.txt`에서 최근 세션 ID 읽기
- `state.json`의 status를 `"stopped"`로 변경
- 종료

**`--resume`인 경우:**
- `specs/latest.txt`에서 최근 세션 ID 읽기
- `state.json`에서 `current_phase` 확인
- 해당 Phase부터 재개

**`--phase N`인 경우:**
- `specs/latest.txt`에서 최근 세션 ID 읽기 (세션 없으면 에러)
- `current_phase`를 N으로 설정
- 해당 Phase부터 실행

**그 외 (기능 설명):**
- 새 세션 ID 생성: `YYYYMMDD_HHMMSS_<feature_slug>`
- `specs/sessions/<id>/` 디렉토리 생성
- `state.json` 초기화
- `specs/latest.txt`에 세션 ID 기록
- Phase 1부터 시작

### 2. Phase 실행

각 Phase 시작 시:
1. `.claude_harness/phases/0N_*.md` 프롬프트 읽기
2. `state.json`의 해당 Phase status를 `"in_progress"`로 업데이트
3. Phase 수행
4. 산출물을 `specs/sessions/<id>/`에 저장
5. `state.json` 업데이트 (status: `"completed"`, 타임스탬프)
6. 다음 Phase로 진행

### 3. Phase별 상세

#### Phase 1 — Clarify (Read-only)
- `docs/SERVICE_BLUEPRINT.md` 읽기
- 요구사항 분석 후 사용자에게 확인 요청
- **사용자 승인 필수** → 승인 후 `01_clarify_summary.md` 저장

#### Phase 2 — Context (Read-only)
- `lib/` 존재 여부 확인 → 없으면 스킵
- 코드베이스 탐색 → `02_context_summary.md` 저장

#### Phase 3 — Plan (Read + Write)
- TASK 분해, 병렬 그룹 정의, 파일 소유권 배정
- **사용자 승인 필수** → 승인 후 `03_plan.md` + `TASK-XXX.md` 저장

#### Phase 4 — Execute (Full) — 병렬 서브에이전트
- `03_plan.md`의 실행 그룹 순서대로 진행
- **각 그룹 내 TASK를 Agent 도구로 동시 실행:**

```
그룹 내 각 TASK에 대해:
  Agent(
    subagent_type = TASK 유형에 맞는 에이전트,
    model = 복잡도에 맞는 모델,
    prompt = "TASK 파일 내용 + 컨텍스트 + 파일 소유권 범위",
    description = "TASK-XXX 실행"
  )
```

- 모든 에이전트를 **하나의 메시지에서 병렬 호출**
- 그룹 완료 후 `dart analyze` 검증
- 에러 시 해당 TASK 에이전트에 수정 위임
- 전체 완료 후 `04_execute_report.md` 저장

#### Phase 5 — Evaluate (Read + Bash)
- Phase 4 맥락 없이 독립 검증
- AC 기반 하나씩 확인
- PASS → 세션 완료
- FAIL → Phase 3으로 루프백 (최대 3회)

### 4. 루프백 처리
- Phase 5에서 FAIL 시:
  - `state.json`의 `loopback_count` 증가
  - 3회 초과면 사용자에게 수동 개입 요청
  - 3회 이하면 Phase 3으로 이동, 실패 항목 기반으로 Plan 수정

### 5. 완료
- Phase 5 PASS 시:
  - `state.json`의 status를 `"completed"`로 변경
  - 최종 요약 출력
