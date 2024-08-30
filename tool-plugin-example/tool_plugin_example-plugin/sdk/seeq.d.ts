export interface SeeqErrorData {
  statusMessage: string;
  errorType?: string;
  errorCategory?: string;
  inaccessible?: string[];
}

// Error object returned from Seeq Workbench when rejecting a promise
export interface SeeqError {
  data: SeeqErrorData;
  status?: number;
  xhrStatus?: string;
}

export interface DateRange {
  start: number; // as unix timestamp in milliseconds
  end: number; // as unix timestamp in milliseconds
  duration: string; // as shown in the workbench
}

export interface Asset {
  id: string;
  name: string;
  formattedName: string;
}

export interface TrendItem {
  id: string;
  name: string;
  dataStatus?: string;
  lastFetchRequest?: string;
  selected: boolean;
  color: string;
  assets: Asset[];
}

export interface TrendSignal extends TrendItem {
  isStringSignal: boolean;
  autoScale: boolean;
  axis: string;
  axisMin: number;
  axisMax: number;
  valueUnitOfMeasure: string;
}

export interface TrendScalar extends TrendItem {
  isStringScalar: boolean;
  autoScale: boolean;
  axis: string;
  axisMin: number;
  axisMax: number;
  valueUnitOfMeasure: string;
}

export interface TrendCondition extends TrendItem {
}

export interface TrendMetric extends TrendItem {
  autoScale: boolean;
  axis: string;
  axisMin: number;
  axisMax: number;
}

export interface TrendTable extends TrendItem {
  stack: boolean;
}

export interface TrendSample {
  key: number;
  value: number | string;
  isUncertain: boolean;
}

export interface DataStatusResults {
  id: string;
  samples?: TrendSample[];
  value?: number | string;
  timingInformation?: string;
  meterInformation?: string;
  valueUnitOfMeasure?: string;
  warningCount?: number;
  warningLogs?: object;
}

export type LogSeverity = 'TRACE' | 'DEBUG' | 'INFO' | 'WARN' | 'ERROR' | 'FATAL';

export type PluginState = object;

export type FormulaArgs = object;

export interface CapsuleProperty {
  /** name of the property (first argument of `setProperty`) */
  name: string;
  /** value of the property in a scalar type */
  value: number | string | boolean;
  /** an optional unit, this is omitted if there is no units or the value is a boolean */
  unitOfMeasure?: string;
}

/** A capsule used in a `condition` formula */
export interface TrendCapsule {
  /** An id may be encoded as a property (CAPSULE_SOURCE_ID_PROPERTY_NAME) in the capsule */
  id?: string;
  startTime: number;
  endTime: number;
  properties: Record<string, any>;
  isUncertain: boolean;
}

export interface RunFormulaArgs {
  start?: string;
  end?: string;
  formula?: string;
  _function?: string;
  parameters?: Record<string, string>;
  fragments?: Record<string, string>;
  limit?: number;
  cancellationGroup?: string;
}

export interface FormulaParameter {
  identifier: string;
  item: {
    id: string;
    name: string;
  };
}

/** A YValue element used in setPointerValues yValues Array */
export interface YValue {
  id: string;
  pointValue: string | number;
}

export interface PluginResponse<T> {
  data: T;
  status: number;
  info: PluginResponseInfo;
}

export interface PluginResponseInfo {
  timingInformation: string;
  meterInformation: string;
}

export interface Workstep {
  id: string;
}

export type Timezone = {
  name: string;
  displayName: string;
  offset: string;
  offsetMinutes: number;
};

export interface PluginInfo {
  category: string;
  identifier: string;
  name: string;
  description?: string;
  host?: any;
  icon?: string;
  options?: any;
  version?: string;
}

export interface SelectedRegion {
  min: number;
  max: number;
}

export interface SelectedRegionOptionTarget {
  selectedOption: string;
  selectedRegion: SelectedRegion;
}

/**
 * Parameters supplied when calling an API
 */
export interface CallApiParams {
  /**
   * The request path
   */
  path: string;
  /**
   * Optional request method (defaults to 'GET')
   */
  method?: 'GET' | 'POST' | 'PUT' | 'DELETE' | 'PATCH';
  /**
   * Optional query parameter
   */
  query?: Record<string, unknown>;
  /**
   * Optional body
   */
  body?: Record<string, unknown>;
  /**
   * Optional headers
   */
  headers?: Record<string, unknown>;
}

/**
 * Parameters supplied when calling a Data Lab API
 */
export interface CallDataLabApiParams extends CallApiParams {
  /**
   * The project ID
   */
  projectId: string;
  /**
   * The name of the Notebook
   */
  notebookName: string;
}

export interface EmailInput {
  /**
   * An array with all the emails that will be added in to field
   */
  to: string[];
  /**
   * An array with all the emails that will be added in cc field
   */
  cc?: string[];
  /**
   * An array with all the emails that will be added in bcc field
   */
  bcc?: string[];
  /**
   * The email subject
   */
  subject: string;
  /**
   * The email body
   */
  body: string;
}

export type DetailsPaneColumnKey = 'axis' | 'autoScale' | 'axisMin' | 'axisMax';

/**
 * The following section contains API types extracted from our Seeq typescript SDK
 */
export interface FormulaRunOutput {
  /**
   * Capsules from the formula result
   */
  capsules?: CapsulesOutput;
  /**
   * Metadata describing the compiled formula's result
   */
  metadata?: Record<string, string>;
  /**
   * Regression output from the formula result. Note that the `table` will also contain values.
   */
  regressionOutput?: RegressionOutput;
  /**
   * The data type of the compiled formula's result
   */
  returnType?: string;
  /**
   * Samples from the formula result
   */
  samples?: GetSamplesOutput;
  /**
   * Scalar from the formula result
   */
  scalar?: ScalarValueOutput;
  /**
   * A plain language status message with information about any issues that may have been encountered during an
   * operation. Null if the status message has not been set.
   */
  statusMessage?: string;
  /**
   * Table from the formula result
   */
  table?: GenericTableOutput;
  /**
   * Contains upgrade information if the formula contains legacy syntax that was automatically updated
   */
  upgradeDetails?: FormulaUpgradeOutput;
  /**
   * Errors (if any) from the formula
   */
  errors?: Array<FormulaCompilerErrorOutput>;
  /**
   * The total number of warnings that have occurred
   */
  warningCount?: number;
  /**
   * The Formula warning logs, which includes the text, line number, and column number where the warning occurred in
   * addition to the warning details
   */
  warningLogs?: Array<FormulaLog>;
}

export interface FormulaCompilerErrorOutput {
  /**
   * The column of the formula that resulted in an error
   */
  column?: number;
  /**
   * The category of the formula error, i.e. when it was encountered
   */
  errorCategory?: string;
  /**
   * The type of formula error that occurred
   */
  errorType?: string;
  /**
   * The function where the error occurred
   */
  functionId?: string;
  /**
   * The line of the formula that resulted in an error
   */
  line?: number;
  /**
   * An error message for the compiled formula
   */
  message?: string;
  /**
   * The itemId that is the cause of the error
   */
  itemId?: string;
}

export interface CapsulesOutput {
  /**
   * The list of capsules
   */
  capsules: Array<Capsule>;
  /**
   * A token that can be used to fetch the next page of results. Submit the same query with the continuationToken set
   * to this returned value. Null if all results have been returned.
   */
  continuationToken?: string;
  /**
   * The unit of measure for the capsule starts and ends. If left empty, input is assumed to be in ISO8601 format.
   */
  keyUnitOfMeasure?: string;
  /**
   * The pagination limit, the total number of collection items that will be returned in this page of results
   */
  limit?: number;
  /**
   * The href of the next set of paginated results
   */
  next?: string;
  /**
   * A plain language status message with information about any issues that may have been encountered during an
   * operation. Null if the status message has not been set.
   */
  statusMessage?: string;
  /**
   * The total number of warnings that have occurred
   */
  warningCount?: number;
  /**
   * The Formula warning logs, which includes the text, line number, and column number where the warning occurred in
   * addition to the warning details
   */
  warningLogs?: Array<FormulaLog>;
}

export interface Capsule {
  /**
   * The point at which the capsule becomes uncertain. For a time, an ISO 8601 date string
   * (YYYY-MM-DDThh:mm:ss.sssssssss±hh:mm), or a whole number of nanoseconds since the unix epoch (if the units are
   * nanoseconds). For a numeric (non-time), a double-precision number.
   */
  cursorKey?: any;
  /**
   * The end of the capsule. For a time, an ISO 8601 date string (YYYY-MM-DDThh:mm:ss.sssssssss±hh:mm), or a whole
   * number of nanoseconds since the unix epoch (if the units are nanoseconds). For a numeric (non-time), a
   * double-precision number.
   */
  end?: any;
  /**
   * The id of the capsule
   */
  id: string;
  /**
   * True if this capsule is fully or partially uncertain
   */
  isUncertain?: boolean;
  /**
   * A list of the capsule's properties
   */
  properties?: Array<ScalarProperty>;
  /**
   * The start of the capsule. For a time, an ISO 8601 date string (YYYY-MM-DDThh:mm:ss.sssssssss±hh:mm), or a whole
   * number of nanoseconds since the unix epoch (if the units are nanoseconds). For a numeric (non-time), a
   * double-precision number.
   */
  start: any;
}

export interface ScalarProperty {
  /**
   * Human readable name.  Null or whitespace names are not permitted
   */
  name: string;
  /**
   * The unit of measure to apply to this property's value. If no unit of measure is set and the value is numeric, it
   * is assumed to be unitless
   */
  unitOfMeasure?: string;
  /**
   * The value to assign to this property. If the value is surrounded by quotes, it is interpreted as a string and no
   * units are set
   */
  value: any;
}

export interface ItemPreviewList {
  /**
   * The list of items requested
   */
  items?: Array<ItemPreview>;
  /**
   * The pagination limit, the total number of collection items that will be returned in this page of results
   */
  limit?: number;
  /**
   * The href of the next set of paginated results
   */
  next?: string;
  /**
   * The pagination offset, the index of the first collection item that will be returned in this page of results
   */
  offset?: number;
  /**
   * The href of the previous set of paginated results
   */
  prev?: string;
  /**
   * A plain language status message with information about any issues that may have been encountered during an
   * operation. Null if the status message has not been set.
   */
  statusMessage?: string;
  /**
   * The total number of items
   */
  totalResults: number;
}

export interface ItemPreview {
  /**
   * The ID that can be used to interact with the item
   */
  id: string;
  /**
   * Whether item is archived
   */
  isArchived?: boolean;
  /**
   * Whether item is redacted
   */
  isRedacted?: boolean;
  /**
   * The human readable name
   */
  name: string;
  /**
   * The type of the item
   */
  type: string;
  /**
   * The item's translation key, if any
   */
  translationKey?: string;
}

export interface RegressionOutput {
  /**
   * The measure of how close the data is to the regression line, adjusted for the number of input signals and samples
   */
  adjustedRSquared: number;
  /**
   * The standard error for the sum squares
   */
  errorSumSquares: number;
  /**
   * The constant offset to add. 0 if forceThroughZero was true. This is the intercept for the output signal rather
   * than the individual coefficients.
   */
  intercept: number;
  /**
   * The standard error for the intercept
   */
  interceptStandardError: number;
  /**
   * True if this regression is uncertain
   */
  isUncertain: boolean;
  /**
   * The measure of how well the model matches the target
   */
  regressionSumSquares: number;
  rSquared?: number;
  /**
   * The value which the regression method suggests for ignoring coefficients
   */
  suggestedPValueCutoff: number;
}

export interface GetSamplesOutput {
  /**
   * A token that can be used to fetch the next page of results. Submit the same query with the continuationToken set
   * to this returned value. Null if all results have been returned.
   */
  continuationToken?: string;
  /**
   * The unit of measure for the series keys
   */
  keyUnitOfMeasure?: string;
  /**
   * The pagination limit, the total number of collection items that will be returned in this page of results
   */
  limit?: number;
  /**
   * The href of the next set of paginated results
   */
  next?: string;
  /**
   * The list of samples
   */
  samples?: Array<SampleOutput>;
  /**
   * A plain language status message with information about any issues that may have been encountered during an
   * operation. Null if the status message has not been set.
   */
  statusMessage?: string;
  /**
   * The unit of measure for the series values
   */
  valueUnitOfMeasure?: string;
  /**
   * The total number of warnings that have occurred
   */
  warningCount?: number;
  /**
   * The Formula warning logs, which includes the text, line number, and column number where the warning occurred in
   * addition to the warning details
   */
  warningLogs?: Array<FormulaLog>;
}

export interface SampleOutput {
  /**
   * True if this sample is uncertain
   */
  isUncertain?: boolean;
  /**
   * The key of the sample. For a time series, an ISO 8601 date string(YYYY-MM-DDThh:mm:ss.sssssssss±hh:mm). For a
   * numeric (non-time) series, a double-precision number.
   */
  key?: any;
  /**
   * The value of the sample
   */
  value?: any;
}

export interface ScalarValueOutput {
  /**
   * True if this scalar is uncertain
   */
  isUncertain?: boolean;
  /**
   * The unit of measure of the scalar
   */
  uom: string;
  /**
   * The value of the scalar
   */
  value: any;
}

export interface ScalarEvaluateOutput {
  /**
   * True if this scalar is uncertain
   */
  isUncertain?: boolean;
  /**
   * Metadata describing the compiled formula's result
   */
  metadata?: Record<string, string>;
  /**
   * The data type of the compiled formula's result
   */
  returnType?: string;
  /**
   * A plain language status message with information about any issues that may have been encountered during an
   * operation. Null if the status message has not been set.
   */
  statusMessage?: string;
  /**
   * The unit of measure of the scalar
   */
  uom: string;
  /**
   * Contains upgrade information if the formula contains legacy syntax that was automatically updated
   */
  upgradeDetails?: FormulaUpgradeOutput;
  /**
   * The value of the scalar
   */
  value: any;
  /**
   * Violations (if any) from the formula
   */
  errors?: Array<FormulaCompilerErrorOutput>;
  /**
   * The total number of warnings that have occurred
   */
  warningCount?: number;
  /**
   * The Formula warning logs, which includes the text, line number, and column number where the warning occurred in
   * addition to the warning details
   */
  warningLogs?: Array<FormulaLog>;
}

export interface GenericTableOutput {
  /**
   * The list of data rows, each row being a list of cell contents.
   */
  data: Array<Array<any>>;
  /**
   * The list of headers.
   */
  headers: Array<TableColumnOutput>;
}

export interface TableColumnOutput {
  /**
   * The name of the column
   */
  name: string;
  /**
   * The type of the column. Valid values include 'string', 'number', and 'date'. Booleans are reported as 'number'
   */
  type: string;
  /**
   * The units of the column. Only provided if type is 'number'
   */
  units?: string;
}

export interface FormulaUpgradeOutput {
  /**
   * The resulting changed formula
   */
  afterFormula?: string;
  /**
   * The original input formula
   */
  beforeFormula?: string;
  /**
   * Details about the specific changes
   */
  changes?: Array<FormulaUpgradeChange>;
  /**
   * The previous version of the formula
   */
  oldVersion?: number;
  /**
   * The new version of the formula
   */
  newVersion?: number;
}

export interface FormulaUpgradeChange {
  /**
   * Description of the change
   */
  change?: string;
  /**
   * A link to the Knowledge Base for more explanation of why this was applied
   */
  moreDetailsUrl?: string;
}

export interface FormulaLog {
  /**
   * The detailed Formula log entries which occurred at this token
   */
  formulaLogEntries: Record<string, FormulaLogEntry>;
  /**
   * The token where the event took place in the Formula
   */
  formulaToken: FormulaToken;
}

export interface FormulaLogEntry {
  logDetails?: Array<FormulaLogEntryDetails>;
  logTypeCount?: number;
}

export interface FormulaLogEntryDetails {
  context?: string;
  message?: string;
}

export interface FormulaToken {
  column?: number;
  line?: number;
  text?: string;
  traceId?: string;
}

export interface ThresholdMetricOutputV1 {
  /**
   * Additional properties of the item
   */
  additionalProperties?: Array<ScalarPropertyV1>;
  /**
   * The ID of the aggregation condition representing metric value information
   */
  aggregationConditionId?: string;
  /**
   * Aggregation formula that aggregates the measured item
   */
  aggregationFunction?: string;
  /**
   * The condition that, if present, will be used to aggregate the measured item
   */
  boundingCondition?: ItemPreviewWithAssetsV1;
  /**
   * The maximum capsule duration that is applied to the bounding condition if it does not have one
   */
  boundingConditionMaximumDuration?: ScalarValueOutputV1;
  /**
   * The data ID of this asset. Note: This is not the Seeq ID, but the unique identifier that the remote datasource
   * uses.
   */
  dataId?: string;
  /**
   * The datasource class, which is the type of system holding the item, such as OSIsoft PI
   */
  datasourceClass?: string;
  /**
   * The datasource identifier, which is how the datasource holding this item identifies itself
   */
  datasourceId?: string;
  /**
   * Clarifying information or other plain language description of this item
   */
  description?: string;
  /**
   * A signal or formula function that evaluates to a signal that can be used to visualize the metric
   */
  displayItem: ItemPreviewV1;
  /**
   * The duration over which to calculate a moving aggregation
   */
  duration?: ScalarValueOutputV1;
  /**
   * The permissions the current user has to the item.
   */
  effectivePermissions?: PermissionsV1;
  /**
   * The ID that can be used to interact with the item
   */
  id: string;
  /**
   * Whether item is archived
   */
  isArchived?: boolean;
  /**
   * Whether item is redacted
   */
  isRedacted?: boolean;
  /**
   * The input Signal or Condition to measure
   */
  measuredItem: ItemPreviewWithAssetsV1;
  /**
   * The human readable name
   */
  name: string;
  /**
   * Either the custom-set neutral color for this metric or the color of the neutral Priority
   */
  neutralColor?: string;
  /**
   * The format string used for numbers associated with this signal.
   */
  numberFormat?: string;
  /**
   * The period at which to sample when creating the moving aggregation
   */
  period?: ScalarValueOutputV1;
  /**
   * The process type of threshold metric. Will be Continuous if duration and period are specified, Condition if
   * boundingCondition is specified, and otherwise Simple.
   */
  processType: ProcessTypeEnum;
  /**
   * The ID of the workbook to which this item is scoped or null if it is in the global scope.
   */
  scopedTo?: string;
  /**
   * A plain language status message with information about any issues that may have been encountered during an
   * operation
   */
  statusMessage?: string;
  /**
   * The list of thresholds that are scalars, signals, or conditions along with the associated priority. These
   * thresholds are those that were used as inputs and which are used to generate the condition thresholds
   */
  thresholds?: Array<ThresholdOutputV1>;
  /**
   * The type of the item
   */
  type: string;
  /**
   * The unit of measure of the metric
   */
  valueUnitOfMeasure?: string;
  /**
   * The item's translation key, if any
   */
  translationKey?: string;
}

export interface ScalarPropertyV1 {
  /**
   * Human readable name.  Null or whitespace names are not permitted
   */
  name: string;
  /**
   * The unit of measure to apply to this property's value. If no unit of measure is set and the value is numeric, it
   * is assumed to be unitless
   */
  unitOfMeasure?: string;
  /**
   * The value to assign to this property. If the value is surrounded by quotes, it is interpreted as a string and no
   * units are set
   */
  value: any;
}

export interface ItemPreviewWithAssetsV1 {
  /**
   * The list of ancestors in the asset tree, ordered with the root ancestor first, if the item is in an asset tree. If
   * an item is in more than one asset tree an arbitrary one will be chosen.
   */
  ancestors?: Array<ItemPreviewV1>;
  /**
   * A boolean indicating whether or not child items exist for this item in the asset tree; the value will be true even
   * if the child items are archived unless the tree for this item is deleted.
   */
  hasChildren?: boolean;
  /**
   * The ID that can be used to interact with the item
   */
  id: string;
  /**
   * Whether item is archived
   */
  isArchived?: boolean;
  /**
   * Whether item is redacted
   */
  isRedacted?: boolean;
  /**
   * The human readable name
   */
  name: string;
  /**
   * The type of the item
   */
  type: string;
  /**
   * The item's translation key, if any
   */
  translationKey?: string;
}

export interface ScalarValueOutputV1 {
  /**
   * True if this scalar is uncertain
   */
  isUncertain?: boolean;
  /**
   * The unit of measure of the scalar
   */
  uom: string;
  /**
   * The value of the scalar
   */
  value: any;
}

export interface ThresholdOutputV1 {
  isGenerated?: boolean;
  /**
   * The threshold item
   */
  item?: ItemPreviewV1;
  /**
   * The priority associated with the threshold. If a custom color has been specified for this threshold it will be set
   * as the color
   */
  priority?: PriorityV1;
  /**
   * The scalar value, only if the item is a scalar
   */
  value?: ScalarValueOutputV1;
}

export interface ItemPreviewV1 {
  /**
   * The ID that can be used to interact with the item
   */
  id: string;
  /**
   * Whether item is archived
   */
  isArchived?: boolean;
  /**
   * Whether item is redacted
   */
  isRedacted?: boolean;
  /**
   * The human readable name
   */
  name: string;
  /**
   * The type of the item
   */
  type: string;
  /**
   * The item's translation key, if any
   */
  translationKey?: string;
}

export interface PermissionsV1 {
  manage?: boolean;
  read?: boolean;
  write?: boolean;
}

export enum ProcessTypeEnum {
  // This is required because the typescript SDK doesn't properly handle enums.
  // @ts-ignore TS1066 (In ambient enum declarations member initializer must be constant expression)
  Simple = 'Simple' as any,
  // @ts-ignore TS1066
  Condition = 'Condition' as any,
  // @ts-ignore TS1066
  Continuous = 'Continuous' as any
}

export interface FormulaLogV1 {
  /**
   * The detailed Formula log entries which occurred at this token
   */
  formulaLogEntries: Record<string, FormulaLogEntry>;
  /**
   * The token where the event took place in the Formula
   */
  formulaToken: FormulaToken;
}

export interface PriorityV1 {
  /**
   * A hex code (including pound sign) representing the color assigned to this priority
   */
  color: string;
  /**
   * An integer representing the priority level. 0 is used for neutral, positive numbers are used for high thresholds
   * and negative numbers for low thresholds
   */
  level: number;
  /**
   * The name of this priority
   */
  name: string;
}

export interface LicensedFeatureStatusOutputV1 {
  /**
   * The number of days left before the current licensed feature will expire
   */
  daysToExpiration?: number;
  /**
   * The licensed feature name
   */
  name?: string;
  /**
   * The final day this licensed feature will be valid for
   */
  validThrough?: string;
  /**
   * Validity status
   */
  validity: ValidityEnum;
}

export enum ValidityEnum {
  // This is required because the typescript SDK doesn't properly handle enums.
  // @ts-ignore TS1066 (In ambient enum declarations member initializer must be constant expression)
  Valid = 'Valid' as any,
  // @ts-ignore TS1066
  NoLicense = 'NoLicense' as any,
  // @ts-ignore TS1066
  Expired = 'Expired' as any,
  // @ts-ignore TS1066
  WrongHost = 'WrongHost' as any,
  // @ts-ignore TS1066
  BadSignature = 'BadSignature' as any,
  // @ts-ignore TS1066
  ClockTampering = 'ClockTampering' as any,
  // @ts-ignore TS1066
  OverLimit = 'OverLimit' as any,
  // @ts-ignore TS1066
  UnknownError = 'UnknownError' as any
}

type WorkstepCallback = (workstep: Workstep) => void;
type StringCallback = (string: string) => void;
type BooleanCallback = (boolean: boolean) => void;
type SelectedRegionCallback = (selectedRegion: SelectedRegion) => void;
type TimezoneCallback = (timezone: Timezone) => void;
type DateRangeCallback = (dateRange: DateRange) => void;
type TrendSignalArrayCallback = (trendSignals: TrendSignal[]) => void;
type TrendScalarArrayCallback = (trendScalars: TrendScalar[]) => void;
type TrendConditionArrayCallback = (trendConditions: TrendCondition[]) => void;
type TrendMetricArrayCallback = (trendMetrics: TrendMetric[]) => void;
type TrendTableArrayCallback = (trendTables: TrendTable[]) => void;
type PluginStateCallback = (pluginState: PluginState) => void;
type SelectedRegionOptionTargetCallback = (selectedRegionOptionTarget: SelectedRegionOptionTarget) => void;
type TrendCapsuleArrayCallback = (trendCapsules: TrendCapsule[]) => void;

type RemoveListener = () => void;

export interface API {
  version: string;

  /**
  * Gets information about the plugin. A subset of the information provided the plugin's plugin.json file.
  */
  pluginInfo: PluginInfo;

  /**
  * The value of an optional query parameter that can be added to the URL of a HomeScreen plugin (aka add-on).
  * This value will be undefined for non-HomeScreen add-ons and HomeScreen add-ons where the query
  * parameter is not supplied. The query parameter is specified by adding a "q" query parameter
  * (e.g. "&q=yourinfohere") to the URL of a HomeScreen add-on.
  */
  queryParam: string;

  /**
  *  Check if the workbench is in presentation mode
  */
  isPresentationWorkbookMode: boolean;

  /**
  *  Check if the workbench is in headless render mode
  */
  isHeadlessRenderMode: boolean;

  /**
  *  Get the active workbook
  */
  workbook: { id: string; name: string; description: string; };

  /**
  *  Get the active worksheet
  */
  worksheet: { id: string; name: string; };

  /**
  *  Subscribe to receive the current workstep ID when it changes
  */
  subscribeToCurrentWorkstep(cb: WorkstepCallback): RemoveListener;

  /**
  *  Subscribe to receive the current user language when it changes
  */
  subscribeToUserLanguage(cb: StringCallback): RemoveListener;

  /**
  *  Subscribe to receive the current dark mode setting
  */
  subscribeToDarkMode(cb: BooleanCallback): RemoveListener;

  /**
  * Subscribe to receive the current trend selected region
  */
  subscribeToTrendSelectedRegion(cb: SelectedRegionCallback): RemoveListener;

  /**
  *  Subscribe to receive the worksheet timezone when it changes
  */
  subscribeToTimezone(cb: TimezoneCallback): RemoveListener;

  /**
  * Expose range selector values
  */
  subscribeToDisplayRange(cb: DateRangeCallback): RemoveListener;
  subscribeToInvestigationRange(cb: DateRangeCallback): RemoveListener;

  /**
  * Subscribe to signals
  */
  subscribeToSignals(cb: TrendSignalArrayCallback): RemoveListener;

  /**
  * Subscribe to scalars
  */
  subscribeToScalars(cb: TrendScalarArrayCallback): RemoveListener;

  /**
  * Subscribe to conditions
  */
  subscribeToConditions(cb: TrendConditionArrayCallback): RemoveListener;

  /**
  * Subscribe to metrics
  */
  subscribeToMetrics(cb: TrendMetricArrayCallback): RemoveListener;

  /**
  * Subscribe to table
  */
  subscribeToTables(cb: TrendTableArrayCallback): RemoveListener;

  /**
  * Updates the display range start and end times. Duration is automatically adjusted to match the new range.
  * If the start time is after the end time, the values are rejected and no change is made.
  *
  * @param start - new start time unix timestamp in milliseconds
  * @param end   - new end time unix timestamp in milliseconds
  */
  setDisplayRange(start: number, end: number): void;

  /**
  * Sets the selected region on the trend
  *
  * @param min - A Unix timestamp for the minimum side of the range in the timezone of the worksheet.
  * @param max - A Unix timestamp for the maximum side of the range in the timezone of the worksheet.
  */
  setTrendSelectedRegion(min: number, max: number): void;

  /**
  * Removes the selected region from the trend
  */
  removeTrendSelectedRegion(): void;

  /**
  * Register options to display when selected region plus icon is clicked
  *
  * @param identifier - The plugin identifier.
  * @param options - The options to display on selected region plus icon.
  */
  registerSelectedRegionOptions(identifier: string, options: string[]): void;

  /**
  * Unregister selected region options
  */
  removeSelectedRegionOptions(): void;

  /**
  * Updates the investigate range start and end times. Duration is automatically adjusted to match the new range.
  * If the start time is after the end time, the values are rejected and no change is made.
  *
  * @param start - new start time unix timestamp in milliseconds
  * @param end   - new end time unix timestamp in milliseconds
  */
  setInvestigateRange(start: number, end: number): void;

  /**
  * Selects an item in the details pane or a capsule in the capsules pane
  *
  * @param id - the id of the item to be selected
  * @param selected - true for selected, false for unselected
  */
  selectItem(id: string, selected: boolean): void;

  /**
  * Log a message that will be saved to the client.log
  */
  log(severity: LogSeverity, message: string): void;

  /**
  * Set plugin state,
  *
  * Note about unloading the plugin: if setPluginState is called during unloading, there is no guarantee that the
  * communication will be finished before the workbench side is dismantled. Plugin authors can rely on state saved
  * that are confirmed via a follow-up plugin state update (via subscribeToPluginState listener).
  *
  * @param pluginState - the state to be set
  */
  setPluginState(pluginState: PluginState): void;

  /**
  * Subscribe to plugin state
  */
  subscribeToPluginState(cb: PluginStateCallback): RemoveListener;

  /**
  * Subscribe to selected region selected/targeted option. When a selected region option is clicked, this updates
  * and shows the newly clicked option and the selected region the new option was clicked for.
  */
  subscribeToSelectedRegionSelectedOption(cb: SelectedRegionOptionTargetCallback): RemoveListener;

  /**
  * Run a Seeq Formula. Stored items (e.g. signals, conditions, scalars) are retrieved by setting the formula to be
  * the parameter name with a leading dollar sign (e.g. $series) and the parameters to an object with the parameter
  * name as the key and ID of the stored item as the value (e.g. { series: "97425979-484E-45FE-B717-A9E55F7DEEBB" }).
  *
  * @example Fetch a stored signal with raw data points
  * runFormula({
  *   start: "2020-06-20T17:20:56.860Z",
  *   end: "2020-06-21T17:20:56.860Z",
  *   formula: "$item",
  *   parameters: { item: "97425979-484E-45FE-B717-A9E55F7DEEBB" }
  *   cancellationGroup: "myCancellationGroup"
  * })
  *
  * @example Run a formula to combine conditions
  * runFormula({
  *   start: "2020-06-20T17:20:56.860Z",
  *   end: "2020-06-21T17:20:56.860Z",
  *   formula: "$a.intersect($b)",
  *   parameters: {
  *     a: "97425979-484E-45FE-B717-A9E55F7DEEBB",
  *     b: "66BA6909-A1F0-4F1C-B529-F5F238E62DC1"
  *   }
  *   cancellationGroup: "myCancellationGroup"
  * })
  *
  * @param {string} [start] - A string representing the starting index of the data to be returned. The contents and
  *   whether or not it is required depends on the result type. For time series: a ISO 8601 timestamp
  *   (YYYY-MM-DDThh:mm:ss.sssssssss±hh:mm). For numeric (non-time) series: a double-precision number, optionally
  *   including units. For example: \&quot;2.5ft\&quot; or \&quot;10 °C\&quot;.
  * @param {string} [end] - A string representing the starting index of the data to be returned. The contents and
  *   whether or not it is required depends on the result type. For time series: a ISO 8601 timestamp
  *   (YYYY-MM-DDThh:mm:ss.sssssssss±hh:mm). For numeric (non-time) series: a double-precision number, optionally
  *   including units. For example: \&quot;2.5ft\&quot; or \&quot;10 °C\&quot;.
  * @param {string} [formula] - The formula to be applied. This or function is required.
  * @param {string} [_function] - The ID of the function item to be computed. This or formula is required.
  * @param {Object} [parameters] - key/value object that the formula can reference
  * @param {Object} [fragments] - A formula fragment object where the keys are the names of unbound formula function
  * variables and the values are the corresponding formula fragments that are used to compute the value of the
  * variable.
  * @param {number} [offset=0] - The pagination offset, the index of the first collection item that will be returned
  *   in this page of results
  * @param {number} [limit=1000] - The pagination limit, the total number of collection items that will be returned in
  *   this page of results
  * @param {string} [cancellationGroup] - a cancellation group name that is used for cancelling the request.
  */
  runFormula({
    start,
    end,
    formula,
    _function,
    parameters,
    fragments,
    limit,
    cancellationGroup,
  }: RunFormulaArgs): Promise<PluginResponse<FormulaRunOutput>>;

  /**
  * Fetch a metric.
  *
  * @param id - the ID of the metric
  */
  fetchMetric(id: string): Promise<PluginResponse<ThresholdMetricOutputV1>>;

  /**
  * Opens a user provided Seeq url (either relative or full path) in a new window.  Only Seeq paths
  * from the same Seeq server as the request are accepted.
  *
  * @param url - The target URL.  It may be a relative or full URL but the origin must match the Seeq Server.
  * @param windowFeatures - https://developer.mozilla.org/en-US/docs/Web/API/Window/open
  */
  openUrl(url: string, windowFeatures: string): void;

  /**
  * Downloads a provided file object
  *
  * @param file - Javascript File Object
  * (https://developer.mozilla.org/en-US/docs/Web/API/File) to download
  */
  downloadContent(file: File): void;

  /**
  * Sets the value in the browser local storage for the given key.
  *
  * @param key - storage key
  * @param value - value
  */
  setItemInLocalStorage(key: string, value: string): void;

  /**
  * Gets the value from the browser local storage for the given key.
  *
  * @param key - storage key
  */
  getItemFromLocalStorage(key: string): Promise<string | null>;

  /**
  * Subscribe to capsules that are selected in the capsules pane
  */
  subscribeToSelectedCapsules(cb: TrendCapsuleArrayCallback): RemoveListener;

  /**
  * Subscribe to capsules in the capsules pane
  */
  subscribeToCapsules(cb: TrendCapsuleArrayCallback): RemoveListener;

  /**
  * Set capsules to be displayed in trend view condition preview
  *
  * @param capsuleSetId - the ID the group of capsules from other groups
  * @param capsules - the list of capsules
  * @param color -  the color code the capsules would be displayed in on the trend view e.g #eb4034
  */
  setTrendCapsulesPreview(capsuleSetId: string, capsules: TrendCapsule[], color: string): void;

  /**
  * Set the data status of an item in the details pane to loading
  *
  * @param id - the ID of the item
  */
  setTrendDataStatusLoading(id: string): void;

  /**
  * Set the data status of an item in the details pane to success
  *
  * @param results - data status results that were returned from the request to fetch the item
  */
  setTrendDataStatusSuccess(results: DataStatusResults): void;

  /**
  * If true, then the plugin is being rendered as part of capturing content for the Organizer.
  */
  shouldProvideOrganizerVisualizationData(): Promise<boolean>;

  /**
  * Provides data to Organizer to be able to render the plugin. The last call to this will be the data that is used.
  *
  * @param data - all of the data needed to render the plugin
  */
  provideOrganizerVisualizationData(data: any): void;

  /**
  * If true, then the plugin is being rendered in Organizer and should load it's data from Organizer by calling
  * [loadDataFromOrganizer]{@link API#loadDataFromOrganizer}.
  */
  shouldLoadDataFromOrganizer(): Promise<boolean>;

  /**
  * Loads the plugin data from Organizer. This will be the exact data was provided by the plugin via
  * [provideOrganizerVisualizationData]{@link API#provideOrganizerVisualizationData}.
  */
  loadDataFromOrganizer(): Promise<any>;

  /**
  * Must be called by the plugin when it has completed it's initial render of plugin content. Lets the screenshot
  * subsystem know when the screenshot can be taken for thumbnails and topic document content.
  */
  pluginRenderComplete(): void;

  /**
  * Sets the x value and y values ​​corresponding to where the mouse pointer is on the chart.
  *
  * @param {number} xValue - The x-value timestamp.
  * @param {YValue[]} yValues - An array of YValue objects for the items on the chart.
  */
  setPointerValues(xValue: number, yValues: YValue[]): void;

  /**
  * Clears the pointer x and y values from the details pane
  */
  clearPointerValues(): void;

  /**
  * Sets the Axis Min and Axis Max values of an item in the details pane
  *
  * @param id - the ID of the item to set
  * @param axisMin - the axis min value
  * @param axisMax - the axis max value
  */
  setYAxis(id: string, axisMin: number, axisMax: number): void;

  /**
  * Sets the Auto property of an item in the details pane
  *
  * @param id - the ID of the item
  * @param autoScale - true to auto scale, false to manually set the scale
  */
  setYAxisAutoScale(id: string, autoScale: boolean): void;

  /**
  * Helper function to be used in conjunction with fetching data for an item that handles non-success responses.
  *
  * @param {String} id - The id of the item
  * @param {String} cancellationGroup - the group name used to count the number of requests
  * @param {Object} error - The error object from the API request
  */
  catchItemDataFailure(id: string, cancellationGroup: string, error: SeeqError): void;

  /**
  * Open the formula tool for edit with the supplied formula and parameters
  */
  editNewFormula(formula: string, parameters: FormulaParameter[]): void;

  /**
  * Close the active investigate Tool
  */
  closeActiveTool(): void;

  /**
  * Shows details pane customization columns
  *
  * @param keys - an array of details pane column keys identifying the columns to be shown
  */
  showDetailsPaneColumns(keys: DetailsPaneColumnKey[]): void;

  /**
  * Returns the details for the licensed feature that matches the specified name. If no feature is found that
  * matches the name, Undefined will be returned.
  *
  * @param {String} name - The name of the licensed features to check for.
  */
  getLicensedFeature(name: string): Promise<LicensedFeatureStatusOutputV1>;

  /**
  * Calls a Seeq SDK API endpoint. This is an EXPERIMENTAL function that may be changed or removed in future
  * versions of Seeq. If you use this capability in your plugin, there is not guarantee that your plugin will
  * work correctly or at all with future versions of Seeq.
  *
  * @param {CallApiParams} params - parameters for the call
  * @param {string} params.path - the request path
  * @param {'GET' | 'POST' | 'PUT' | 'DELETE' | 'PATCH'} [params.method] - optional request method (defaults to 'GET')
  * @param {Record<string, unknown>} [params.query] - optional query parameters
  * @param {Record<string, unknown>} [params.body] - optional body
  * @param {Record<string, unknown>} [params.headers] - optional headers
  * @return {Promise<T>} The response of the API call
  */
  callSdkApi<T = any>(params: CallApiParams): Promise<T>;

  /**
  * Calls a Seeq Data Lab API endpoint
  *
  * @param {CallDataLabApiParams} params - parameters for the call
  * @param {string} params.projectId - the project ID
  * @param {string} params.notebookName - the notebook name
  * @param {string} params.path - the request path
  * @param {'GET' | 'POST' | 'PUT' | 'DELETE' | 'PATCH'} [params.method] - optional request method (defaults to 'GET')
  * @param {Record<string, unknown>} [params.query] - optional query parameters
  * @param {Record<string, unknown>} [params.body] - optional body
  * @param {Record<string, unknown>} [params.headers] - optional headers
  * @return {Promise<T>} The response of the API call
  */
  callDataLabApi<T = any>(params: CallDataLabApiParams): Promise<T>;

  /**
  * Returns the ID of the single Data Lab Project that matches the supplied name.
  * The returned promise will reject if zero or more-than-one projects are found with the same name.
  * The creator of the project must ensure that the name is unique on the server.
  *
  * @param {string} projectName - Project name
  * @return {Promise<{ projectId: string }>} The ID of the project
  */
  getDataLabProject(projectName: string): Promise<{ projectId: string }>;

  /**
  * Open default email client and display a custom message.
  *
  * @param {EmailInput} emailInput - the to, Cc, Bcc, subject, and body
  */
  mailTo(emailInput: EmailInput): void;
}

export function getSeeqApi(): Promise<API>;
