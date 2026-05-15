import Std

inductive Verdict where
  | pass
  | warn
  | block
  deriving DecidableEq, Repr

def verdictRank : Verdict -> Nat
  | Verdict.pass => 0
  | Verdict.warn => 1
  | Verdict.block => 2

def isSafeInterval (upperBound limit : Int) : Bool :=
  if upperBound <= limit then true else false

def isBlockedInterval (upperBound limit : Int) : Bool :=
  if upperBound > limit then true else false

def intervalVerdict (upperBound limit warnMargin : Int) : Verdict :=
  if upperBound > limit then Verdict.block
  else if upperBound > limit - warnMargin then Verdict.warn
  else Verdict.pass

theorem strictBlockEnforcement (upperBound limit : Int) :
    upperBound > limit ->
    isBlockedInterval upperBound limit = true := by
  intro h
  simp [isBlockedInterval, h]

theorem passEnforcement (upperBound limit : Int) :
    upperBound <= limit ->
    isSafeInterval upperBound limit = true := by
  intro h
  simp [isSafeInterval, h]

theorem blockVerdictCorrect (upperBound limit warnMargin : Int) :
    upperBound > limit ->
    intervalVerdict upperBound limit warnMargin = Verdict.block := by
  intro h
  simp [intervalVerdict, h]

theorem passVerdictCorrect
    (upperBound limit warnMargin : Int) :
    0 <= warnMargin ->
    upperBound <= limit - warnMargin ->
    intervalVerdict upperBound limit warnMargin = Verdict.pass := by
  intro hMargin hPass
  have hNotBlock : Not (upperBound > limit) := by
    omega
  have hNotWarn : Not (upperBound > limit - warnMargin) := by
    omega
  simp [intervalVerdict, hNotBlock, hNotWarn]

theorem warnVerdictCorrect
    (upperBound limit warnMargin : Int) :
    upperBound > limit - warnMargin ->
    upperBound <= limit ->
    intervalVerdict upperBound limit warnMargin = Verdict.warn := by
  intro hWarn hNotBlock
  have hNoBlock : Not (upperBound > limit) := by
    omega
  simp [intervalVerdict, hNoBlock, hWarn]

theorem warnVerdictOnlyWithinBand
    (upperBound limit warnMargin : Int) :
    intervalVerdict upperBound limit warnMargin = Verdict.warn ->
    limit - warnMargin < upperBound /\ upperBound <= limit := by
  unfold intervalVerdict
  by_cases hBlock : upperBound > limit
  · simp [hBlock]
  · by_cases hWarn : upperBound > limit - warnMargin
    · intro _
      constructor <;> omega
    · simp [hBlock, hWarn]

theorem deterministicSafetyBool (upperBound limit : Int) :
    Or
      (isSafeInterval upperBound limit = true)
      (isSafeInterval upperBound limit = false) := by
  cases isSafeInterval upperBound limit <;> simp

theorem deterministicBlockBool (upperBound limit : Int) :
    Or
      (isBlockedInterval upperBound limit = true)
      (isBlockedInterval upperBound limit = false) := by
  cases isBlockedInterval upperBound limit <;> simp

theorem deterministicVerdict
    (upperBound limit warnMargin : Int) :
    Or
      (intervalVerdict upperBound limit warnMargin = Verdict.pass)
      (Or
        (intervalVerdict upperBound limit warnMargin = Verdict.warn)
        (intervalVerdict upperBound limit warnMargin = Verdict.block)) := by
  unfold intervalVerdict
  split
  · exact Or.inr (Or.inr rfl)
  · split
    · exact Or.inr (Or.inl rfl)
    · exact Or.inl rfl

theorem verdictMonotoneWithUpperBound
    (lowerUpper upperBound limit warnMargin : Int) :
    lowerUpper <= upperBound ->
    verdictRank (intervalVerdict lowerUpper limit warnMargin) <=
      verdictRank (intervalVerdict upperBound limit warnMargin) := by
  intro hOrder
  by_cases hUpperBlock : upperBound > limit
  · by_cases hLowerBlock : lowerUpper > limit
    · simp [intervalVerdict, hUpperBlock, hLowerBlock, verdictRank]
    · by_cases hLowerWarn : lowerUpper > limit - warnMargin
      · simp [intervalVerdict, hUpperBlock, hLowerBlock, hLowerWarn, verdictRank]
      · simp [intervalVerdict, hUpperBlock, hLowerBlock, hLowerWarn, verdictRank]
  · have hLowerNotBlock : Not (lowerUpper > limit) := by
      omega
    by_cases hUpperWarn : upperBound > limit - warnMargin
    · by_cases hLowerWarn : lowerUpper > limit - warnMargin
      · simp [
          intervalVerdict,
          hUpperBlock,
          hUpperWarn,
          hLowerNotBlock,
          hLowerWarn,
          verdictRank,
        ]
      · simp [
          intervalVerdict,
          hUpperBlock,
          hUpperWarn,
          hLowerNotBlock,
          hLowerWarn,
          verdictRank,
        ]
    · have hLowerNotWarn : Not (lowerUpper > limit - warnMargin) := by
        omega
      simp [
        intervalVerdict,
        hUpperBlock,
        hUpperWarn,
        hLowerNotBlock,
        hLowerNotWarn,
        verdictRank,
      ]
