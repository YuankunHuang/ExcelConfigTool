// <auto-generated>
//     Generated by the protocol buffer compiler.  DO NOT EDIT!
//     source: Sample1.proto
// </auto-generated>
#pragma warning disable 1591, 0612, 3021, 8981
#region Designer generated code

using pb = global::Google.Protobuf;
using pbc = global::Google.Protobuf.Collections;
using pbr = global::Google.Protobuf.Reflection;
using scg = global::System.Collections.Generic;
/// <summary>Holder for reflection information generated from Sample1.proto</summary>
public static partial class Sample1Reflection {

  #region Descriptor
  /// <summary>File descriptor for Sample1.proto</summary>
  public static pbr::FileDescriptor Descriptor {
    get { return descriptor; }
  }
  private static pbr::FileDescriptor descriptor;

  static Sample1Reflection() {
    byte[] descriptorData = global::System.Convert.FromBase64String(
        string.Concat(
          "Cg1TYW1wbGUxLnByb3RvGh9nb29nbGUvcHJvdG9idWYvdGltZXN0YW1wLnBy",
          "b3RvIogBCgpTYW1wbGUxUm93EgoKAmlkGAEgASgFEgwKBG5hbWUYAiABKAkS",
          "DQoFbGV2ZWwYAyABKAMSEAoIaXNBY3RpdmUYBCABKAgSEAoIdGVzdE51bGwY",
          "BSABKAkSLQoJc3RhcnRUaW1lGAYgASgLMhouZ29vZ2xlLnByb3RvYnVmLlRp",
          "bWVzdGFtcCIkCgdTYW1wbGUxEhkKBHJvd3MYASADKAsyCy5TYW1wbGUxUm93",
          "YgZwcm90bzM="));
    descriptor = pbr::FileDescriptor.FromGeneratedCode(descriptorData,
        new pbr::FileDescriptor[] { global::Google.Protobuf.WellKnownTypes.TimestampReflection.Descriptor, },
        new pbr::GeneratedClrTypeInfo(null, null, new pbr::GeneratedClrTypeInfo[] {
          new pbr::GeneratedClrTypeInfo(typeof(global::Sample1Row), global::Sample1Row.Parser, new[]{ "Id", "Name", "Level", "IsActive", "TestNull", "StartTime" }, null, null, null, null),
          new pbr::GeneratedClrTypeInfo(typeof(global::Sample1), global::Sample1.Parser, new[]{ "Rows" }, null, null, null, null)
        }));
  }
  #endregion

}
#region Messages
[global::System.Diagnostics.DebuggerDisplayAttribute("{ToString(),nq}")]
public sealed partial class Sample1Row : pb::IMessage<Sample1Row>
#if !GOOGLE_PROTOBUF_REFSTRUCT_COMPATIBILITY_MODE
    , pb::IBufferMessage
#endif
{
  private static readonly pb::MessageParser<Sample1Row> _parser = new pb::MessageParser<Sample1Row>(() => new Sample1Row());
  private pb::UnknownFieldSet _unknownFields;
  [global::System.Diagnostics.DebuggerNonUserCodeAttribute]
  [global::System.CodeDom.Compiler.GeneratedCode("protoc", null)]
  public static pb::MessageParser<Sample1Row> Parser { get { return _parser; } }

  [global::System.Diagnostics.DebuggerNonUserCodeAttribute]
  [global::System.CodeDom.Compiler.GeneratedCode("protoc", null)]
  public static pbr::MessageDescriptor Descriptor {
    get { return global::Sample1Reflection.Descriptor.MessageTypes[0]; }
  }

  [global::System.Diagnostics.DebuggerNonUserCodeAttribute]
  [global::System.CodeDom.Compiler.GeneratedCode("protoc", null)]
  pbr::MessageDescriptor pb::IMessage.Descriptor {
    get { return Descriptor; }
  }

  [global::System.Diagnostics.DebuggerNonUserCodeAttribute]
  [global::System.CodeDom.Compiler.GeneratedCode("protoc", null)]
  public Sample1Row() {
    OnConstruction();
  }

  partial void OnConstruction();

  [global::System.Diagnostics.DebuggerNonUserCodeAttribute]
  [global::System.CodeDom.Compiler.GeneratedCode("protoc", null)]
  public Sample1Row(Sample1Row other) : this() {
    id_ = other.id_;
    name_ = other.name_;
    level_ = other.level_;
    isActive_ = other.isActive_;
    testNull_ = other.testNull_;
    startTime_ = other.startTime_ != null ? other.startTime_.Clone() : null;
    _unknownFields = pb::UnknownFieldSet.Clone(other._unknownFields);
  }

  [global::System.Diagnostics.DebuggerNonUserCodeAttribute]
  [global::System.CodeDom.Compiler.GeneratedCode("protoc", null)]
  public Sample1Row Clone() {
    return new Sample1Row(this);
  }

  /// <summary>Field number for the "id" field.</summary>
  public const int IdFieldNumber = 1;
  private int id_;
  [global::System.Diagnostics.DebuggerNonUserCodeAttribute]
  [global::System.CodeDom.Compiler.GeneratedCode("protoc", null)]
  public int Id {
    get { return id_; }
    set {
      id_ = value;
    }
  }

  /// <summary>Field number for the "name" field.</summary>
  public const int NameFieldNumber = 2;
  private string name_ = "";
  [global::System.Diagnostics.DebuggerNonUserCodeAttribute]
  [global::System.CodeDom.Compiler.GeneratedCode("protoc", null)]
  public string Name {
    get { return name_; }
    set {
      name_ = pb::ProtoPreconditions.CheckNotNull(value, "value");
    }
  }

  /// <summary>Field number for the "level" field.</summary>
  public const int LevelFieldNumber = 3;
  private long level_;
  [global::System.Diagnostics.DebuggerNonUserCodeAttribute]
  [global::System.CodeDom.Compiler.GeneratedCode("protoc", null)]
  public long Level {
    get { return level_; }
    set {
      level_ = value;
    }
  }

  /// <summary>Field number for the "isActive" field.</summary>
  public const int IsActiveFieldNumber = 4;
  private bool isActive_;
  [global::System.Diagnostics.DebuggerNonUserCodeAttribute]
  [global::System.CodeDom.Compiler.GeneratedCode("protoc", null)]
  public bool IsActive {
    get { return isActive_; }
    set {
      isActive_ = value;
    }
  }

  /// <summary>Field number for the "testNull" field.</summary>
  public const int TestNullFieldNumber = 5;
  private string testNull_ = "";
  [global::System.Diagnostics.DebuggerNonUserCodeAttribute]
  [global::System.CodeDom.Compiler.GeneratedCode("protoc", null)]
  public string TestNull {
    get { return testNull_; }
    set {
      testNull_ = pb::ProtoPreconditions.CheckNotNull(value, "value");
    }
  }

  /// <summary>Field number for the "startTime" field.</summary>
  public const int StartTimeFieldNumber = 6;
  private global::Google.Protobuf.WellKnownTypes.Timestamp startTime_;
  [global::System.Diagnostics.DebuggerNonUserCodeAttribute]
  [global::System.CodeDom.Compiler.GeneratedCode("protoc", null)]
  public global::Google.Protobuf.WellKnownTypes.Timestamp StartTime {
    get { return startTime_; }
    set {
      startTime_ = value;
    }
  }

  [global::System.Diagnostics.DebuggerNonUserCodeAttribute]
  [global::System.CodeDom.Compiler.GeneratedCode("protoc", null)]
  public override bool Equals(object other) {
    return Equals(other as Sample1Row);
  }

  [global::System.Diagnostics.DebuggerNonUserCodeAttribute]
  [global::System.CodeDom.Compiler.GeneratedCode("protoc", null)]
  public bool Equals(Sample1Row other) {
    if (ReferenceEquals(other, null)) {
      return false;
    }
    if (ReferenceEquals(other, this)) {
      return true;
    }
    if (Id != other.Id) return false;
    if (Name != other.Name) return false;
    if (Level != other.Level) return false;
    if (IsActive != other.IsActive) return false;
    if (TestNull != other.TestNull) return false;
    if (!object.Equals(StartTime, other.StartTime)) return false;
    return Equals(_unknownFields, other._unknownFields);
  }

  [global::System.Diagnostics.DebuggerNonUserCodeAttribute]
  [global::System.CodeDom.Compiler.GeneratedCode("protoc", null)]
  public override int GetHashCode() {
    int hash = 1;
    if (Id != 0) hash ^= Id.GetHashCode();
    if (Name.Length != 0) hash ^= Name.GetHashCode();
    if (Level != 0L) hash ^= Level.GetHashCode();
    if (IsActive != false) hash ^= IsActive.GetHashCode();
    if (TestNull.Length != 0) hash ^= TestNull.GetHashCode();
    if (startTime_ != null) hash ^= StartTime.GetHashCode();
    if (_unknownFields != null) {
      hash ^= _unknownFields.GetHashCode();
    }
    return hash;
  }

  [global::System.Diagnostics.DebuggerNonUserCodeAttribute]
  [global::System.CodeDom.Compiler.GeneratedCode("protoc", null)]
  public override string ToString() {
    return pb::JsonFormatter.ToDiagnosticString(this);
  }

  [global::System.Diagnostics.DebuggerNonUserCodeAttribute]
  [global::System.CodeDom.Compiler.GeneratedCode("protoc", null)]
  public void WriteTo(pb::CodedOutputStream output) {
  #if !GOOGLE_PROTOBUF_REFSTRUCT_COMPATIBILITY_MODE
    output.WriteRawMessage(this);
  #else
    if (Id != 0) {
      output.WriteRawTag(8);
      output.WriteInt32(Id);
    }
    if (Name.Length != 0) {
      output.WriteRawTag(18);
      output.WriteString(Name);
    }
    if (Level != 0L) {
      output.WriteRawTag(24);
      output.WriteInt64(Level);
    }
    if (IsActive != false) {
      output.WriteRawTag(32);
      output.WriteBool(IsActive);
    }
    if (TestNull.Length != 0) {
      output.WriteRawTag(42);
      output.WriteString(TestNull);
    }
    if (startTime_ != null) {
      output.WriteRawTag(50);
      output.WriteMessage(StartTime);
    }
    if (_unknownFields != null) {
      _unknownFields.WriteTo(output);
    }
  #endif
  }

  #if !GOOGLE_PROTOBUF_REFSTRUCT_COMPATIBILITY_MODE
  [global::System.Diagnostics.DebuggerNonUserCodeAttribute]
  [global::System.CodeDom.Compiler.GeneratedCode("protoc", null)]
  void pb::IBufferMessage.InternalWriteTo(ref pb::WriteContext output) {
    if (Id != 0) {
      output.WriteRawTag(8);
      output.WriteInt32(Id);
    }
    if (Name.Length != 0) {
      output.WriteRawTag(18);
      output.WriteString(Name);
    }
    if (Level != 0L) {
      output.WriteRawTag(24);
      output.WriteInt64(Level);
    }
    if (IsActive != false) {
      output.WriteRawTag(32);
      output.WriteBool(IsActive);
    }
    if (TestNull.Length != 0) {
      output.WriteRawTag(42);
      output.WriteString(TestNull);
    }
    if (startTime_ != null) {
      output.WriteRawTag(50);
      output.WriteMessage(StartTime);
    }
    if (_unknownFields != null) {
      _unknownFields.WriteTo(ref output);
    }
  }
  #endif

  [global::System.Diagnostics.DebuggerNonUserCodeAttribute]
  [global::System.CodeDom.Compiler.GeneratedCode("protoc", null)]
  public int CalculateSize() {
    int size = 0;
    if (Id != 0) {
      size += 1 + pb::CodedOutputStream.ComputeInt32Size(Id);
    }
    if (Name.Length != 0) {
      size += 1 + pb::CodedOutputStream.ComputeStringSize(Name);
    }
    if (Level != 0L) {
      size += 1 + pb::CodedOutputStream.ComputeInt64Size(Level);
    }
    if (IsActive != false) {
      size += 1 + 1;
    }
    if (TestNull.Length != 0) {
      size += 1 + pb::CodedOutputStream.ComputeStringSize(TestNull);
    }
    if (startTime_ != null) {
      size += 1 + pb::CodedOutputStream.ComputeMessageSize(StartTime);
    }
    if (_unknownFields != null) {
      size += _unknownFields.CalculateSize();
    }
    return size;
  }

  [global::System.Diagnostics.DebuggerNonUserCodeAttribute]
  [global::System.CodeDom.Compiler.GeneratedCode("protoc", null)]
  public void MergeFrom(Sample1Row other) {
    if (other == null) {
      return;
    }
    if (other.Id != 0) {
      Id = other.Id;
    }
    if (other.Name.Length != 0) {
      Name = other.Name;
    }
    if (other.Level != 0L) {
      Level = other.Level;
    }
    if (other.IsActive != false) {
      IsActive = other.IsActive;
    }
    if (other.TestNull.Length != 0) {
      TestNull = other.TestNull;
    }
    if (other.startTime_ != null) {
      if (startTime_ == null) {
        StartTime = new global::Google.Protobuf.WellKnownTypes.Timestamp();
      }
      StartTime.MergeFrom(other.StartTime);
    }
    _unknownFields = pb::UnknownFieldSet.MergeFrom(_unknownFields, other._unknownFields);
  }

  [global::System.Diagnostics.DebuggerNonUserCodeAttribute]
  [global::System.CodeDom.Compiler.GeneratedCode("protoc", null)]
  public void MergeFrom(pb::CodedInputStream input) {
  #if !GOOGLE_PROTOBUF_REFSTRUCT_COMPATIBILITY_MODE
    input.ReadRawMessage(this);
  #else
    uint tag;
    while ((tag = input.ReadTag()) != 0) {
    if ((tag & 7) == 4) {
      // Abort on any end group tag.
      return;
    }
    switch(tag) {
        default:
          _unknownFields = pb::UnknownFieldSet.MergeFieldFrom(_unknownFields, input);
          break;
        case 8: {
          Id = input.ReadInt32();
          break;
        }
        case 18: {
          Name = input.ReadString();
          break;
        }
        case 24: {
          Level = input.ReadInt64();
          break;
        }
        case 32: {
          IsActive = input.ReadBool();
          break;
        }
        case 42: {
          TestNull = input.ReadString();
          break;
        }
        case 50: {
          if (startTime_ == null) {
            StartTime = new global::Google.Protobuf.WellKnownTypes.Timestamp();
          }
          input.ReadMessage(StartTime);
          break;
        }
      }
    }
  #endif
  }

  #if !GOOGLE_PROTOBUF_REFSTRUCT_COMPATIBILITY_MODE
  [global::System.Diagnostics.DebuggerNonUserCodeAttribute]
  [global::System.CodeDom.Compiler.GeneratedCode("protoc", null)]
  void pb::IBufferMessage.InternalMergeFrom(ref pb::ParseContext input) {
    uint tag;
    while ((tag = input.ReadTag()) != 0) {
    if ((tag & 7) == 4) {
      // Abort on any end group tag.
      return;
    }
    switch(tag) {
        default:
          _unknownFields = pb::UnknownFieldSet.MergeFieldFrom(_unknownFields, ref input);
          break;
        case 8: {
          Id = input.ReadInt32();
          break;
        }
        case 18: {
          Name = input.ReadString();
          break;
        }
        case 24: {
          Level = input.ReadInt64();
          break;
        }
        case 32: {
          IsActive = input.ReadBool();
          break;
        }
        case 42: {
          TestNull = input.ReadString();
          break;
        }
        case 50: {
          if (startTime_ == null) {
            StartTime = new global::Google.Protobuf.WellKnownTypes.Timestamp();
          }
          input.ReadMessage(StartTime);
          break;
        }
      }
    }
  }
  #endif

}

[global::System.Diagnostics.DebuggerDisplayAttribute("{ToString(),nq}")]
public sealed partial class Sample1 : pb::IMessage<Sample1>
#if !GOOGLE_PROTOBUF_REFSTRUCT_COMPATIBILITY_MODE
    , pb::IBufferMessage
#endif
{
  private static readonly pb::MessageParser<Sample1> _parser = new pb::MessageParser<Sample1>(() => new Sample1());
  private pb::UnknownFieldSet _unknownFields;
  [global::System.Diagnostics.DebuggerNonUserCodeAttribute]
  [global::System.CodeDom.Compiler.GeneratedCode("protoc", null)]
  public static pb::MessageParser<Sample1> Parser { get { return _parser; } }

  [global::System.Diagnostics.DebuggerNonUserCodeAttribute]
  [global::System.CodeDom.Compiler.GeneratedCode("protoc", null)]
  public static pbr::MessageDescriptor Descriptor {
    get { return global::Sample1Reflection.Descriptor.MessageTypes[1]; }
  }

  [global::System.Diagnostics.DebuggerNonUserCodeAttribute]
  [global::System.CodeDom.Compiler.GeneratedCode("protoc", null)]
  pbr::MessageDescriptor pb::IMessage.Descriptor {
    get { return Descriptor; }
  }

  [global::System.Diagnostics.DebuggerNonUserCodeAttribute]
  [global::System.CodeDom.Compiler.GeneratedCode("protoc", null)]
  public Sample1() {
    OnConstruction();
  }

  partial void OnConstruction();

  [global::System.Diagnostics.DebuggerNonUserCodeAttribute]
  [global::System.CodeDom.Compiler.GeneratedCode("protoc", null)]
  public Sample1(Sample1 other) : this() {
    rows_ = other.rows_.Clone();
    _unknownFields = pb::UnknownFieldSet.Clone(other._unknownFields);
  }

  [global::System.Diagnostics.DebuggerNonUserCodeAttribute]
  [global::System.CodeDom.Compiler.GeneratedCode("protoc", null)]
  public Sample1 Clone() {
    return new Sample1(this);
  }

  /// <summary>Field number for the "rows" field.</summary>
  public const int RowsFieldNumber = 1;
  private static readonly pb::FieldCodec<global::Sample1Row> _repeated_rows_codec
      = pb::FieldCodec.ForMessage(10, global::Sample1Row.Parser);
  private readonly pbc::RepeatedField<global::Sample1Row> rows_ = new pbc::RepeatedField<global::Sample1Row>();
  [global::System.Diagnostics.DebuggerNonUserCodeAttribute]
  [global::System.CodeDom.Compiler.GeneratedCode("protoc", null)]
  public pbc::RepeatedField<global::Sample1Row> Rows {
    get { return rows_; }
  }

  [global::System.Diagnostics.DebuggerNonUserCodeAttribute]
  [global::System.CodeDom.Compiler.GeneratedCode("protoc", null)]
  public override bool Equals(object other) {
    return Equals(other as Sample1);
  }

  [global::System.Diagnostics.DebuggerNonUserCodeAttribute]
  [global::System.CodeDom.Compiler.GeneratedCode("protoc", null)]
  public bool Equals(Sample1 other) {
    if (ReferenceEquals(other, null)) {
      return false;
    }
    if (ReferenceEquals(other, this)) {
      return true;
    }
    if(!rows_.Equals(other.rows_)) return false;
    return Equals(_unknownFields, other._unknownFields);
  }

  [global::System.Diagnostics.DebuggerNonUserCodeAttribute]
  [global::System.CodeDom.Compiler.GeneratedCode("protoc", null)]
  public override int GetHashCode() {
    int hash = 1;
    hash ^= rows_.GetHashCode();
    if (_unknownFields != null) {
      hash ^= _unknownFields.GetHashCode();
    }
    return hash;
  }

  [global::System.Diagnostics.DebuggerNonUserCodeAttribute]
  [global::System.CodeDom.Compiler.GeneratedCode("protoc", null)]
  public override string ToString() {
    return pb::JsonFormatter.ToDiagnosticString(this);
  }

  [global::System.Diagnostics.DebuggerNonUserCodeAttribute]
  [global::System.CodeDom.Compiler.GeneratedCode("protoc", null)]
  public void WriteTo(pb::CodedOutputStream output) {
  #if !GOOGLE_PROTOBUF_REFSTRUCT_COMPATIBILITY_MODE
    output.WriteRawMessage(this);
  #else
    rows_.WriteTo(output, _repeated_rows_codec);
    if (_unknownFields != null) {
      _unknownFields.WriteTo(output);
    }
  #endif
  }

  #if !GOOGLE_PROTOBUF_REFSTRUCT_COMPATIBILITY_MODE
  [global::System.Diagnostics.DebuggerNonUserCodeAttribute]
  [global::System.CodeDom.Compiler.GeneratedCode("protoc", null)]
  void pb::IBufferMessage.InternalWriteTo(ref pb::WriteContext output) {
    rows_.WriteTo(ref output, _repeated_rows_codec);
    if (_unknownFields != null) {
      _unknownFields.WriteTo(ref output);
    }
  }
  #endif

  [global::System.Diagnostics.DebuggerNonUserCodeAttribute]
  [global::System.CodeDom.Compiler.GeneratedCode("protoc", null)]
  public int CalculateSize() {
    int size = 0;
    size += rows_.CalculateSize(_repeated_rows_codec);
    if (_unknownFields != null) {
      size += _unknownFields.CalculateSize();
    }
    return size;
  }

  [global::System.Diagnostics.DebuggerNonUserCodeAttribute]
  [global::System.CodeDom.Compiler.GeneratedCode("protoc", null)]
  public void MergeFrom(Sample1 other) {
    if (other == null) {
      return;
    }
    rows_.Add(other.rows_);
    _unknownFields = pb::UnknownFieldSet.MergeFrom(_unknownFields, other._unknownFields);
  }

  [global::System.Diagnostics.DebuggerNonUserCodeAttribute]
  [global::System.CodeDom.Compiler.GeneratedCode("protoc", null)]
  public void MergeFrom(pb::CodedInputStream input) {
  #if !GOOGLE_PROTOBUF_REFSTRUCT_COMPATIBILITY_MODE
    input.ReadRawMessage(this);
  #else
    uint tag;
    while ((tag = input.ReadTag()) != 0) {
    if ((tag & 7) == 4) {
      // Abort on any end group tag.
      return;
    }
    switch(tag) {
        default:
          _unknownFields = pb::UnknownFieldSet.MergeFieldFrom(_unknownFields, input);
          break;
        case 10: {
          rows_.AddEntriesFrom(input, _repeated_rows_codec);
          break;
        }
      }
    }
  #endif
  }

  #if !GOOGLE_PROTOBUF_REFSTRUCT_COMPATIBILITY_MODE
  [global::System.Diagnostics.DebuggerNonUserCodeAttribute]
  [global::System.CodeDom.Compiler.GeneratedCode("protoc", null)]
  void pb::IBufferMessage.InternalMergeFrom(ref pb::ParseContext input) {
    uint tag;
    while ((tag = input.ReadTag()) != 0) {
    if ((tag & 7) == 4) {
      // Abort on any end group tag.
      return;
    }
    switch(tag) {
        default:
          _unknownFields = pb::UnknownFieldSet.MergeFieldFrom(_unknownFields, ref input);
          break;
        case 10: {
          rows_.AddEntriesFrom(ref input, _repeated_rows_codec);
          break;
        }
      }
    }
  }
  #endif

}

#endregion


#endregion Designer generated code
