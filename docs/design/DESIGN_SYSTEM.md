# Design System

이 문서는 프로젝트의 디자인 시스템 마스터 문서입니다.
프론트엔드 구축/수정 시 반드시 이 문서를 참조하세요.

> 이 문서를 수정하면 `design_tokens.json`도 함께 동기화해야 합니다.

---

## 1. Color Palette

### Brand Colors
| 이름 | HEX | 용도 |
|------|-----|------|
| Primary | #000000 | 메인 액션, CTA 버튼 |
| Secondary | #000000 | 보조 액션, 강조 |
| Tertiary | #000000 | 서브 요소 |

### Neutral Colors
| 이름 | HEX | 용도 |
|------|-----|------|
| Background | #FFFFFF | 기본 배경 |
| Surface | #F5F5F5 | 카드, 시트 배경 |
| Border | #E0E0E0 | 구분선, 테두리 |
| TextPrimary | #1A1A1A | 본문 텍스트 |
| TextSecondary | #757575 | 보조 텍스트 |
| Disabled | #BDBDBD | 비활성 상태 |

### Semantic Colors
| 이름 | HEX | 용도 |
|------|-----|------|
| Success | #4CAF50 | 성공 상태 |
| Warning | #FF9800 | 경고 상태 |
| Error | #F44336 | 에러 상태 |
| Info | #2196F3 | 정보 안내 |

---

## 2. Typography

| 스타일 | 크기 | 두께 | 행간 | 용도 |
|--------|------|------|------|------|
| Heading1 | 28sp | Bold (700) | 1.3 | 페이지 제목 |
| Heading2 | 22sp | SemiBold (600) | 1.3 | 섹션 제목 |
| Heading3 | 18sp | SemiBold (600) | 1.3 | 서브 제목 |
| Body1 | 16sp | Regular (400) | 1.5 | 본문 |
| Body2 | 14sp | Regular (400) | 1.5 | 보조 본문 |
| Caption | 12sp | Regular (400) | 1.4 | 캡션, 라벨 |
| Button | 16sp | SemiBold (600) | 1.0 | 버튼 텍스트 |

**Font Family**: 시스템 기본 (또는 지정 폰트명)

---

## 3. Spacing & Sizing

### Spacing Scale
| 토큰 | 값 | 용도 |
|------|----|------|
| xs | 4dp | 아이콘-텍스트 간격 |
| sm | 8dp | 관련 요소 간 간격 |
| md | 16dp | 섹션 내 간격, 기본 패딩 |
| lg | 24dp | 섹션 간 간격 |
| xl | 32dp | 큰 영역 간 구분 |
| xxl | 48dp | 페이지 상하 여백 |

### Border Radius
| 토큰 | 값 | 용도 |
|------|----|------|
| none | 0 | 직각 |
| sm | 4dp | 입력 필드 |
| md | 8dp | 카드, 버튼 |
| lg | 16dp | 바텀시트, 모달 |
| full | 999dp | 원형 (아바타, 뱃지) |

---

## 4. Components

### Button
| 타입 | 배경 | 텍스트 | 높이 | Radius |
|------|------|--------|------|--------|
| Primary | Primary | White | 48dp | md |
| Secondary | Transparent | Primary | 48dp | md |
| Text | Transparent | Primary | 40dp | none |
| Disabled | Disabled | White | 48dp | md |

### Input Field
- 높이: 48dp
- 패딩: md (16dp)
- Border: 1dp Border색, radius sm
- Focus: Primary색 border
- Error: Error색 border + 하단 에러 텍스트 (Caption, Error색)

### Card
- 패딩: md (16dp)
- Radius: md (8dp)
- 배경: Surface
- 그림자: elevation 1~2

### AppBar
- 높이: 56dp
- 배경: Background
- 제목: Heading3, TextPrimary
- 하단 구분선: Border 1dp

### BottomNavigationBar
- 높이: 64dp
- 활성 아이콘/텍스트: Primary
- 비활성 아이콘/텍스트: TextSecondary

---

## 5. Iconography
- 아이콘 셋: Material Icons (또는 지정 아이콘 셋)
- 기본 크기: 24dp
- 색상: 컨텍스트에 따라 TextPrimary / TextSecondary / Primary

---

## 6. 상태별 UI 패턴

### Loading
- 중앙 CircularProgressIndicator (Primary색)
- Skeleton shimmer (선택)

### Empty
- 중앙 아이콘 (64dp, TextSecondary) + 안내 텍스트 (Body2, TextSecondary)

### Error
- 중앙 아이콘 (64dp, Error) + 에러 메시지 + 재시도 버튼

---

## 7. Animation
- 기본 duration: 300ms
- 기본 curve: Curves.easeInOut
- 페이지 전환: SlideTransition 또는 FadeTransition
