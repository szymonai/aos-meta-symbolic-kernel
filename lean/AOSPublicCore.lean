import Std

inductive Verdict where
  | pass
  | warn
  | block
  deriving DecidableEq, Repr

inductive EvidenceLevel where
  | e1
  | e2
  | e3ProtocolRun
  | e3
  deriving DecidableEq, Repr

inductive PublicEvidenceLevel where
  | notE3
  | e3Protocol
  | e3Effectiveness
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

structure JsonGateInput where
  score : Int
  uncertainty : Int
  limit : Int
  warnMargin : Int
  metadataComplete : Bool
  deriving DecidableEq, Repr

structure AuditDecision where
  expected : Verdict
  observed : Verdict
  digestPresent : Bool
  replayed : Bool
  deriving DecidableEq, Repr

structure StudyCriteria where
  scenarioCount : Nat
  frozenModelOutputs : Bool
  datasetSourcesNamed : Bool
  sourceSplitsPresent : Bool
  modelOutputHashesValid : Bool
  sourceRecordHashesPresent : Bool
  recordIdsUnique : Bool
  outputGenerationMetadataPresent : Bool
  labelingProtocolPresent : Bool
  categoriesCovered : Bool
  difficultyD1D9Covered : Bool
  minimumCasesPerCategory : Bool
  minimumCasesPerDifficulty : Bool
  comparatorsNamed : Bool
  metricsPredefined : Bool
  caseLevelResultsIncluded : Bool
  scenarioHashIncluded : Bool
  replaySucceeded : Bool
  auditCoverageComplete : Bool
  deriving DecidableEq, Repr

structure EffectivenessCriteria where
  independentSignalExtraction : Bool
  labelsNotUsedAsSignals : Bool
  normalizationLayerEvaluated : Bool
  heldOutManualAuditPresent : Bool
  baselineInputsMatched : Bool
  failureCasesReported : Bool
  tradeoffMetricsReported : Bool
  deriving DecidableEq, Repr

def JsonGateInput.upperBound (input : JsonGateInput) : Int :=
  input.score + input.uncertainty

def auditDecisionReady (decision : AuditDecision) : Bool :=
  decision.digestPresent && decision.replayed

def silentBlockPassThrough (decision : AuditDecision) : Prop :=
  decision.expected = Verdict.block ∧ decision.observed = Verdict.pass

def studyDesignReady (criteria : StudyCriteria) : Bool :=
  decide (500 <= criteria.scenarioCount) &&
    criteria.frozenModelOutputs &&
    criteria.datasetSourcesNamed &&
    criteria.sourceSplitsPresent &&
    criteria.outputGenerationMetadataPresent &&
    criteria.labelingProtocolPresent &&
    criteria.categoriesCovered &&
    criteria.difficultyD1D9Covered &&
    criteria.minimumCasesPerCategory &&
    criteria.minimumCasesPerDifficulty &&
    criteria.comparatorsNamed &&
    criteria.metricsPredefined

def studyAuditReady (criteria : StudyCriteria) : Bool :=
  criteria.modelOutputHashesValid &&
    criteria.sourceRecordHashesPresent &&
    criteria.recordIdsUnique &&
    criteria.caseLevelResultsIncluded &&
    criteria.scenarioHashIncluded &&
    criteria.replaySucceeded &&
    criteria.auditCoverageComplete

def e3Ready (criteria : StudyCriteria) : Bool :=
  studyDesignReady criteria && studyAuditReady criteria

def studyEvidenceLevel (criteria : StudyCriteria) : EvidenceLevel :=
  if e3Ready criteria then EvidenceLevel.e3 else EvidenceLevel.e3ProtocolRun

def effectivenessReady (criteria : EffectivenessCriteria) : Bool :=
  criteria.independentSignalExtraction &&
    criteria.labelsNotUsedAsSignals &&
    criteria.normalizationLayerEvaluated &&
    criteria.heldOutManualAuditPresent &&
    criteria.baselineInputsMatched &&
    criteria.failureCasesReported &&
    criteria.tradeoffMetricsReported

def publicEvidenceLevel
    (criteria : StudyCriteria)
    (effectiveness : EffectivenessCriteria) : PublicEvidenceLevel :=
  if e3Ready criteria then
    if effectivenessReady effectiveness then
      PublicEvidenceLevel.e3Effectiveness
    else
      PublicEvidenceLevel.e3Protocol
  else
    PublicEvidenceLevel.notE3

def jsonInputWellFormed (input : JsonGateInput) : Prop :=
  0 <= input.score ∧
    0 <= input.uncertainty ∧
    0 <= input.limit ∧
    0 <= input.warnMargin ∧
    input.warnMargin < input.limit

def jsonGateVerdict (input : JsonGateInput) : Verdict :=
  if input.metadataComplete then
    intervalVerdict input.upperBound input.limit input.warnMargin
  else
    Verdict.block

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

theorem jsonInputUpperBoundMatchesFields (input : JsonGateInput) :
    input.upperBound = input.score + input.uncertainty := by
  rfl

theorem auditDecisionReadyHasDigest
    (decision : AuditDecision) :
    auditDecisionReady decision = true ->
    decision.digestPresent = true := by
  intro h
  simp [auditDecisionReady] at h
  exact h.1

theorem auditDecisionReadyHasReplay
    (decision : AuditDecision) :
    auditDecisionReady decision = true ->
    decision.replayed = true := by
  intro h
  simp [auditDecisionReady] at h
  exact h.2

theorem exactBlockDecisionNotSilent
    (decision : AuditDecision) :
    decision.expected = Verdict.block ->
    decision.observed = decision.expected ->
    Not (silentBlockPassThrough decision) := by
  intro hExpected hExact hSilent
  have hObservedBlock : decision.observed = Verdict.block := by
    rw [hExact, hExpected]
  have hObservedPass : decision.observed = Verdict.pass := hSilent.2
  rw [hObservedBlock] at hObservedPass
  contradiction

theorem e3AssessmentSound
    (criteria : StudyCriteria) :
    e3Ready criteria = true ->
    studyEvidenceLevel criteria = EvidenceLevel.e3 := by
  intro hReady
  simp [studyEvidenceLevel, hReady]

theorem e3AssessmentDoesNotOverclaim
    (criteria : StudyCriteria) :
    e3Ready criteria = false ->
    studyEvidenceLevel criteria = EvidenceLevel.e3ProtocolRun := by
  intro hReady
  simp [studyEvidenceLevel, hReady]

theorem publicEffectivenessEvidenceRequiresProtocol
    (criteria : StudyCriteria)
    (effectiveness : EffectivenessCriteria) :
    publicEvidenceLevel criteria effectiveness =
      PublicEvidenceLevel.e3Effectiveness ->
    e3Ready criteria = true := by
  intro h
  by_cases hReady : e3Ready criteria = true
  · exact hReady
  · simp [publicEvidenceLevel, hReady] at h

theorem publicEffectivenessEvidenceRequiresEffectivenessReady
    (criteria : StudyCriteria)
    (effectiveness : EffectivenessCriteria) :
    publicEvidenceLevel criteria effectiveness =
      PublicEvidenceLevel.e3Effectiveness ->
    effectivenessReady effectiveness = true := by
  intro h
  by_cases hReady : e3Ready criteria = true
  · simp [publicEvidenceLevel, hReady] at h
    by_cases hEffectiveness : effectivenessReady effectiveness = true
    · exact hEffectiveness
    · simp [hEffectiveness] at h
  · simp [publicEvidenceLevel, hReady] at h

theorem labelMappingBlocksEffectivenessReady
    (criteria : EffectivenessCriteria) :
    criteria.labelsNotUsedAsSignals = false ->
    effectivenessReady criteria = false := by
  intro h
  simp [effectivenessReady, h]

theorem e3ReadyRequiresAudit
    (criteria : StudyCriteria) :
    e3Ready criteria = true ->
    studyAuditReady criteria = true := by
  intro hReady
  simp [e3Ready] at hReady
  exact hReady.2

theorem e3ReadyRequiresDesign
    (criteria : StudyCriteria) :
    e3Ready criteria = true ->
    studyDesignReady criteria = true := by
  intro hReady
  simp [e3Ready] at hReady
  exact hReady.1

theorem missingMinimumCasesBlocksE3
    (criteria : StudyCriteria) :
    criteria.scenarioCount < 500 ->
    e3Ready criteria = false := by
  intro hCount
  have hMinimum : decide (500 <= criteria.scenarioCount) = false := by
    simp [Nat.not_le_of_gt hCount]
  simp [e3Ready, studyDesignReady, hMinimum]

theorem jsonWellFormedHasNonnegativeUncertainty
    (input : JsonGateInput) :
    jsonInputWellFormed input ->
    0 <= input.uncertainty := by
  intro h
  exact h.2.1

theorem jsonWellFormedWarnMarginBelowLimit
    (input : JsonGateInput) :
    jsonInputWellFormed input ->
    input.warnMargin < input.limit := by
  intro h
  exact h.2.2.2.2

theorem jsonIncompleteInputBlocks
    (input : JsonGateInput) :
    input.metadataComplete = false ->
    jsonGateVerdict input = Verdict.block := by
  intro h
  simp [jsonGateVerdict, h]

theorem jsonCompleteInputUsesIntervalVerdict
    (input : JsonGateInput) :
    input.metadataComplete = true ->
    jsonGateVerdict input =
      intervalVerdict input.upperBound input.limit input.warnMargin := by
  intro h
  simp [jsonGateVerdict, h]

theorem jsonCompleteBlockCorrect
    (input : JsonGateInput) :
    input.metadataComplete = true ->
    input.upperBound > input.limit ->
    jsonGateVerdict input = Verdict.block := by
  intro hMeta hBlock
  simp [jsonGateVerdict, hMeta, intervalVerdict, hBlock]

theorem jsonCompleteWarnCorrect
    (input : JsonGateInput) :
    input.metadataComplete = true ->
    input.upperBound > input.limit - input.warnMargin ->
    input.upperBound <= input.limit ->
    jsonGateVerdict input = Verdict.warn := by
  intro hMeta hWarn hLimit
  have hNoBlock : Not (input.upperBound > input.limit) := by
    omega
  simp [jsonGateVerdict, hMeta, intervalVerdict, hNoBlock, hWarn]

theorem jsonCompletePassCorrect
    (input : JsonGateInput) :
    input.metadataComplete = true ->
    0 <= input.warnMargin ->
    input.upperBound <= input.limit - input.warnMargin ->
    jsonGateVerdict input = Verdict.pass := by
  intro hMeta hMargin hPass
  have hNotBlock : Not (input.upperBound > input.limit) := by
    omega
  have hNotWarn : Not (input.upperBound > input.limit - input.warnMargin) := by
    omega
  simp [jsonGateVerdict, hMeta, intervalVerdict, hNotBlock, hNotWarn]

theorem jsonGateVerdictDeterministic
    (input : JsonGateInput) :
    Or
      (jsonGateVerdict input = Verdict.pass)
      (Or
        (jsonGateVerdict input = Verdict.warn)
        (jsonGateVerdict input = Verdict.block)) := by
  cases hMeta : input.metadataComplete
  · simp [jsonGateVerdict, hMeta]
  · simpa [jsonGateVerdict, hMeta] using
      deterministicVerdict input.upperBound input.limit input.warnMargin

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
