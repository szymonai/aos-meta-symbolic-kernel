def isSafeInterval (value uncertainty limit : Int) : Bool :=
  if value + uncertainty <= limit then true else false

def isBlockedInterval (value uncertainty limit : Int) : Bool :=
  if value + uncertainty > limit then true else false

def intervalVerdict (value uncertainty limit warnMargin : Int) : String :=
  if value + uncertainty > limit then "BLOCK"
  else if value + uncertainty > limit - warnMargin then "WARN"
  else "PASS"

theorem strictBlockEnforcement (value uncertainty limit : Int) :
    value + uncertainty > limit ->
    isBlockedInterval value uncertainty limit = true := by
  intro h
  simp [isBlockedInterval, h]

theorem passEnforcement (value uncertainty limit : Int) :
    value + uncertainty <= limit ->
    isSafeInterval value uncertainty limit = true := by
  intro h
  simp [isSafeInterval, h]

theorem blockVerdictCorrect (value uncertainty limit warnMargin : Int) :
    value + uncertainty > limit ->
    intervalVerdict value uncertainty limit warnMargin = "BLOCK" := by
  intro h
  simp [intervalVerdict, h]

theorem warnVerdictCorrect (value uncertainty limit warnMargin : Int) :
    Not (value + uncertainty > limit) ->
    value + uncertainty > limit - warnMargin ->
    intervalVerdict value uncertainty limit warnMargin = "WARN" := by
  intro hNotBlock hWarn
  simp [intervalVerdict, hNotBlock, hWarn]

theorem passVerdictCorrect (value uncertainty limit warnMargin : Int) :
    Not (value + uncertainty > limit) ->
    Not (value + uncertainty > limit - warnMargin) ->
    intervalVerdict value uncertainty limit warnMargin = "PASS" := by
  intro hNotBlock hNotWarn
  simp [intervalVerdict, hNotBlock, hNotWarn]

theorem deterministicSafetyBool (value uncertainty limit : Int) :
    Or
      (isSafeInterval value uncertainty limit = true)
      (isSafeInterval value uncertainty limit = false) := by
  cases isSafeInterval value uncertainty limit <;> simp

theorem deterministicBlockBool (value uncertainty limit : Int) :
    Or
      (isBlockedInterval value uncertainty limit = true)
      (isBlockedInterval value uncertainty limit = false) := by
  cases isBlockedInterval value uncertainty limit <;> simp

theorem deterministicVerdict
    (value uncertainty limit warnMargin : Int) :
    Or
      (intervalVerdict value uncertainty limit warnMargin = "PASS")
      (Or
        (intervalVerdict value uncertainty limit warnMargin = "WARN")
        (intervalVerdict value uncertainty limit warnMargin = "BLOCK")) := by
  unfold intervalVerdict
  split
  · exact Or.inr (Or.inr rfl)
  · split
    · exact Or.inr (Or.inl rfl)
    · exact Or.inl rfl
