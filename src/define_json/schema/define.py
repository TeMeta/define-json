from __future__ import annotations 

import re
import sys
from datetime import (
    date,
    datetime,
    time
)
from decimal import Decimal 
from enum import Enum 
from typing import (
    Any,
    ClassVar,
    Literal,
    Optional,
    Union
)

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    RootModel,
    field_validator
)


metamodel_version = "None"
version = "None"


class ConfiguredBaseModel(BaseModel):
    model_config = ConfigDict(
        validate_assignment = True,
        validate_default = True,
        extra = "forbid",
        arbitrary_types_allowed = True,
        use_enum_values = True,
        strict = False,
    )
    pass




class LinkMLMeta(RootModel):
    root: dict[str, Any] = {}
    model_config = ConfigDict(frozen=True)

    def __getattr__(self, key:str):
        return getattr(self.root, key)

    def __getitem__(self, key:str):
        return self.root[key]

    def __setitem__(self, key:str, value):
        self.root[key] = value

    def __contains__(self, key:str) -> bool:
        return key in self.root


linkml_meta = LinkMLMeta({'default_prefix': 'odm',
     'description': 'Data model for supply and demand data contracts to complement '
                    'CDISC USDM, ODM, and Dataset-JSON. This LinkML version '
                    'includes semantics to act as Rosetta Stone for SDMX, FHIR, '
                    'OMOP, RDF, and CDISC.',
     'id': 'https://cdisc.org/define-json',
     'imports': ['linkml:types'],
     'license': 'MIT',
     'name': 'Define-JSON',
     'prefixes': {'dcat': {'prefix_prefix': 'dcat',
                           'prefix_reference': 'http://www.w3.org/ns/dcat#'},
                  'dct': {'prefix_prefix': 'dct',
                          'prefix_reference': 'http://purl.org/dc/terms/'},
                  'dprod': {'prefix_prefix': 'dprod',
                            'prefix_reference': 'https://ekgf.github.io/dprod/'},
                  'fhir': {'prefix_prefix': 'fhir',
                           'prefix_reference': 'http://hl7.org/fhir/'},
                  'linkml': {'prefix_prefix': 'linkml',
                             'prefix_reference': 'https://w3id.org/linkml/'},
                  'odm': {'prefix_prefix': 'odm',
                          'prefix_reference': 'https://cdisc.org/odm2/'},
                  'omop': {'prefix_prefix': 'omop',
                           'prefix_reference': 'https://omop.org/omop-cdm/'},
                  'osb': {'prefix_prefix': 'osb',
                          'prefix_reference': 'https://openstudybuilder.com/'},
                  'prov': {'prefix_prefix': 'prov',
                           'prefix_reference': 'http://www.w3.org/ns/prov#'},
                  'qb': {'prefix_prefix': 'qb',
                         'prefix_reference': 'http://purl.org/linked-data/cube#'},
                  'sdmx': {'prefix_prefix': 'sdmx',
                           'prefix_reference': 'http://purl.org/linked-data/sdmx#'},
                  'sdtm': {'prefix_prefix': 'sdtm',
                           'prefix_reference': 'https://cdisc.org/cosmos/sdtm_v1.0#'},
                  'skos': {'prefix_prefix': 'skos',
                           'prefix_reference': 'http://www.w3.org/2004/02/skos/core#'},
                  'usdm': {'prefix_prefix': 'usdm',
                           'prefix_reference': 'https://cdisc.org/usdm/'}},
     'source_file': 'define.yaml'} )

class AliasPredicate(str, Enum):
    """
    An enumeration that defines permissible values for the relationship between an element and its alias
    """
    EXACT_SYNONYM = "EXACT_SYNONYM"
    """
    Codes have identical meaning e.g. "diabetes mellitus" and "DM"
    """
    RELATED_SYNONYM = "RELATED_SYNONYM"
    """
    Codes are related but not equivalent e.g. "diabetes" and "mellitus"
    """
    BROAD_SYNONYM = "BROAD_SYNONYM"
    """
    Target is broader than source e.g. "diabetes" is broader than "type 2 diabetes"
    """
    NARROW_SYNONYM = "NARROW_SYNONYM"
    """
    Target is narrower than source e.g. "type 2 diabetes" is narrower than "diabetes"
    """


class Comparator(str, Enum):
    """
    An enumeration that defines the types of comparison operations available for a RangeCheck
    """
    LT = "LT"
    """
    Less than
    """
    LE = "LE"
    """
    Less than or equal
    """
    GT = "GT"
    """
    Greater than
    """
    GE = "GE"
    """
    Greater than or equal
    """
    EQ = "EQ"
    """
    Equal
    """
    NE = "NE"
    """
    Not equal
    """
    IN = "IN"
    """
    In set
    """
    NOTIN = "NOTIN"
    """
    Not in set
    """


class UserType(str, Enum):
    """
    An enumeration that defines the types of users in a clinical data collection or management system
    """
    Sponsor = "Sponsor"
    Investigator = "Investigator"
    Lab = "Lab"
    Other = "Other"
    Subject = "Subject"
    Monitor = "Monitor"
    Data_analyst = "Data analyst"
    Care_provider = "Care provider"
    Assessor = "Assessor"


class OrganizationType(str, Enum):
    """
    An enumeration that defines the types of organizations involved in clinical research
    """
    Sponsor = "Sponsor"
    Site = "Site"
    CRO = "CRO"
    Lab = "Lab"
    TechnologyProvider = "TechnologyProvider"
    Other = "Other"


class SoftHard(str, Enum):
    """
    An enumeration that indicates whether a validation check should be treated as an error or a warning
    """
    Soft = "Soft"
    """
    Warning
    """
    Hard = "Hard"
    """
    Error
    """


class MethodType(str, Enum):
    """
    An enumeration that defines the types of computational methods available for data processing
    """
    Computation = "Computation"
    """
    Mathematical computation using values of other items.
    """
    Imputation = "Imputation"
    """
    Assignment of a value based on a estimation (imputation) procedure.
    """
    Transformation = "Transformation"
    """
    Transformation of the item's value according to a standard algorithm, such as a change in units.
    """
    Analysis = "Analysis"
    """
    Creation of analysis results dataset.
    """
    Display = "Display"
    """
    Creation of rendered output for display.
    """


class DataType(str, Enum):
    """
    An enumeration that defines the fundamental data types available for items
    """
    text = "text"
    """
    Character text with no length restriction.
    """
    integer = "integer"
    """
    Integer numbers.
    """
    float = "float"
    """
    Floating-point numbers (decimals).
    """
    date = "date"
    """
    Calendar date.
    """
    time = "time"
    """
    Time of day.
    """
    datetime = "datetime"
    """
    Calendar date and time of day.
    """
    boolean = "boolean"
    """
    Logical values (true/false).
    """
    double = "double"
    """
    Double-precision floating-point numbers.
    """
    hex = "hex"
    """
    Hexadecimal number.
    """
    base64 = "base64"
    """
    Base-64 encoded binary data.
    """
    hexBinary = "hexBinary"
    """
    Hexadecimal encoded binary data.
    """


class OriginType(str, Enum):
    """
    An enumeration that defines the types of origins for data items.
    """
    Assigned = "Assigned"
    """
    A value that is derived through designation, such as values from a look up table or a label on a CRF.
    """
    Collected = "Collected"
    """
    A value that is actually observed and recorded by a person or obtained by an instrument.
    """
    Derived = "Derived"
    """
    A value that is calculated by an algorithm or reproducible rule, and which is dependent upon other data values.
    """
    Not_Available = "Not Available"
    """
    A value that is not discoverable or accessible.
    """
    Other = "Other"
    """
    Different than the one(s) previously specified or mentioned. (NCI)
    """
    Predecessor = "Predecessor"
    """
    A value that is copied from another variable.
    """
    Protocol = "Protocol"
    """
    A value that is included as part of the study protocol.
    """


class OriginSource(str, Enum):
    """
    An enumeration that defines the sources of data origin
    """
    Investigator = "Investigator"
    Sponsor = "Sponsor"
    Subject = "Subject"
    Vendor = "Vendor"


class ItemGroupType(str, Enum):
    """
    An enumeration that defines the roles of an item group within a specific context
    """
    DataCube = "DataCube"
    """
    A Data Structure Definition for an Analysis Data Cube of dimensions, measures, and attributes.
    """
    Table = "Table"
    """
    A simple table or data frame.
    """
    Object = "Object"
    """
    An object or profile of a FHIR resource.
    """
    DatasetSpecialization = "DatasetSpecialization"
    """
    A data specialization of a concept.
    """
    ValueList = "ValueList"
    """
    A list of topic-specific items for a specific column (from Define-XML).
    """
    Section = "Section"
    """
    A section of a form.
    """
    Form = "Form"
    """
    A data collection form.
    """


class TimingType(str, Enum):
    """
    An enumeration that defines CDISC timing type values indicating the temporal relationship of an observation to a reference point
    """
    After = "After"
    Before = "Before"
    Fixed = "Fixed"


class LinkingPhraseEnum(str, Enum):
    """
    An enumeration that defines variable relationship descriptive linking phrases from the COSMoS SDTM BC model
    """
    assesses_seriousness_of = "assesses seriousness of"
    assesses_the_severity_of = "assesses the severity of"
    associates_the_tumor_identified_in = "associates the tumor identified in"
    decodes_the_value_in = "decodes the value in"
    describes_actions_taken = "describes actions taken"
    describes_relationship_of = "describes relationship of"
    describes_the_outcome_of = "describes the outcome of"
    further_describes_the_test_in = "further describes the test in"
    further_specifies_the_anatomical_location_in = "further specifies the anatomical location in"
    groups_tumor_assessments_used_in_overall_response_identified_by = "groups tumor assessments used in overall response identified by"
    groups_values_in = "groups values in"
    groups_within_an_individual_subject_values_in = "groups, within an individual subject, values in"
    identifies_a_pattern_of = "identifies a pattern of"
    identifies_an_observation_described_by = "identifies an observation described by"
    identifies_overall_response_supported_by_tumor_assessments_identified_by = "identifies overall response supported by tumor assessments identified by"
    identifies_the_image_from_the_procedure_in = "identifies the image from the procedure in"
    identifies_the_tumor_found_by_the_test_in = "identifies the tumor found by the test in"
    indicates_occurrence_of_the_value_in = "indicates occurrence of the value in"
    indicates_pre_specification_of_the_value_in = "indicates pre-specification of the value in"
    indicates_severity_of = "indicates severity of"
    indicates_the_previous_irradiation_status_of_the_tumor_identified_by = "indicates the previous irradiation status of the tumor identified by"
    indicates_the_progression_status_of_the_previous_irradiated_tumor_identified_by = "indicates the progression status of the previous irradiated tumor identified by"
    is_a_dictionary_derived_term_for_the_value_in = "is a dictionary-derived term for the value in"
    is_a_dictionary_derived_class_code_for_the_value_in = "is a dictionary-derived class code for the value in"
    is_a_dictionary_derived_class_name_for_the_value_in = "is a dictionary-derived class name for the value in"
    is_decoded_by_the_value_in = "is decoded by the value in"
    is_original_text_for = "is original text for"
    is_the_administered_amount_of_the_treatment_in = "is the administered amount of the treatment in"
    is_the_administration_anatomical_location_for_the_treatment_in = "is the administration anatomical location for the treatment in"
    is_the_aspect_of_the_event_used_to_define_the_date_in = "is the aspect of the event used to define the date in"
    is_the_clinical_significance_interpretation_for = "is the clinical significance interpretation for"
    is_the_code_for_the_value_in = "is the code for the value in"
    is_the_dictionary_code_for_the_test_in = "is the dictionary code for the test in"
    is_the_dictionary_derived_term_for_the_value_in = "is the dictionary-derived term for the value in"
    is_the_dictionary_derived_class_code_for_the_value_in = "is the dictionary-derived class code for the value in"
    is_the_dictionary_derived_class_name_for_the_value_in = "is the dictionary-derived class name for the value in"
    is_the_duration_for = "is the duration for"
    is_the_end_date_for = "is the end date for"
    is_the_epoch_of_the_performance_of_the_test_in = "is the epoch of the performance of the test in"
    is_the_frequency_of_administration_of_the_amount_in = "is the frequency of administration of the amount in"
    is_the_identifier_for_the_source_data_used_in_the_performance_of_the_test_in = "is the identifier for the source data used in the performance of the test in"
    is_the_material_type_of_the_subject_of_the_activity_in = "is the material type of the subject of the activity in"
    is_the_medical_condition_that_is_the_reason_for_the_treatment_in = "is the medical condition that is the reason for the treatment in"
    is_the_method_for_the_test_in = "is the method for the test in"
    is_the_part_of_the_body_through_which_is_administered_the_treatment_in = "is the part of the body through which is administered the treatment in"
    is_the_physical_form_of_the_product_in = "is the physical form of the product in"
    is_the_result_of_the_test_in = "is the result of the test in"
    is_the_role_of_the_assessor_who_performed_the_test_in = "is the role of the assessor who performed the test in"
    is_the_specimen_tested_in = "is the specimen tested in"
    is_the_start_date_for = "is the start date for"
    is_the_subject_position_during_performance_of_the_test_in = "is the subject position during performance of the test in"
    is_the_subjectAPOSTROPHEs_fasting_status_during_the_performance_of_the_test_in = "is the subject's fasting status during the performance of the test in"
    is_the_unit_for_the_value_in = "is the unit for the value in"
    is_the_unit_for = "is the unit for"
    specifies_the_anatomical_location_in = "specifies the anatomical location in"
    specifies_the_anatomical_location_of = "specifies the anatomical location of"
    specifies_the_anatomical_location_of_the_performance_of_the_test_in = "specifies the anatomical location of the performance of the test in"
    specifies_the_anatomical_location_of_the_tumor_identified_by = "specifies the anatomical location of the tumor identified by"
    specifies_the_severity_of = "specifies the severity of"
    values_are_grouped_by = "values are grouped by"
    was_the_subject_position_during_performance_of_the_test_in = "was the subject position during performance of the test in"
    identifies_the_reference_used_in_the_genomic_test_in = "identifies the reference used in the genomic test in"
    indicates_heritability_of_the_genetic_variant_in = "indicates heritability of the genetic variant in"
    is_an_identifier_for_a_published_reference_for_the_genetic_variant_in = "is an identifier for a published reference for the genetic variant in"
    is_an_identifier_for_the_copy_on_one_of_two_homologous_chromosones_of_the_genetic_variant_in = "is an identifier for the copy, on one of two homologous chromosones, of the genetic variant in"
    is_an_identifier_for_the_genetic_sequence_of_the_genetic_entity_represented_by = "is an identifier for the genetic sequence of the genetic entity represented by"
    is_the_chromosome_that_is_the_position_of_the_result_in = "is the chromosome that is the position of the result in"
    is_the_clinical_trial_or_treatment_setting_for = "is the clinical trial or treatment setting for"
    is_the_date_of_occurrence = "is the date of occurrence"
    is_the_date_of_occurrence_for = "is the date of occurrence for"
    is_the_intended_disease_outcome_for = "is the intended disease outcome for"
    is_the_method_of_secondary_analysis_of_results_in = "is the method of secondary analysis of results in"
    is_the_numeric_location_within_a_chromosone_genetic_entity_or_genetic_sub_region_of_the_result_in = "is the numeric location, within a chromosone, genetic entity, or genetic sub-region, of the result in"
    is_the_symbol_for_the_genomic_entity_that_is_the_position_of_the_result_in = "is the symbol for the genomic entity that is the position of the result in"
    is_the_type_of_genomic_entity_that_is_the_position_of_the_result_in = "is the type of genomic entity that is the position of the result in"
    is_the_genetic_sub_location_of_the_result_in = "is the genetic sub-location of the result in"
    is_the_object_of_the_observation_in = "is the object of the observation in"
    is_an_identifier_for_the_evaluator_with_the_role_in = "is an identifier for the evaluator with the role in"
    is_the_severity_of_the_toxicity_in = "is the severity of the toxicity in"
    is_a_grouping_of_values_in = "is a grouping of values in"
    is_the_textual_description_of_the_intended_dose_regimen_for = "is the textual description of the intended dose regimen for"
    is_the_reason_for_stopping_administration_of = "is the reason for stopping administration of"
    is_the_value_of_the_property_identified_by = "is the value of the property identified by"
    is_the_name_of_the_reference_terminology_for = "is the name of the reference terminology for"
    is_the_version_of_the_reference_terminology_in = "is the version of the reference terminology in"


class PredicateTermEnum(str, Enum):
    """
    An enumeration that defines short variable relationship linking phrases for programming purposes from the COSMoS SDTM BC model
    """
    ASSESSES = "ASSESSES"
    CLASSIFIES = "CLASSIFIES"
    DECODES = "DECODES"
    DESCRIBES = "DESCRIBES"
    GROUPS = "GROUPS"
    GROUPS_BY = "GROUPS_BY"
    IDENTIFIES = "IDENTIFIES"
    IDENTIFIES_OBSERVATION = "IDENTIFIES_OBSERVATION"
    IDENTIFIES_PRODUCT_IN = "IDENTIFIES_PRODUCT_IN"
    IDENTIFIES_TUMOR_IN = "IDENTIFIES_TUMOR_IN"
    INDICATES = "INDICATES"
    IS_ATTRIBUTE_FOR = "IS_ATTRIBUTE_FOR"
    IS_DECODED_BY = "IS_DECODED_BY"
    IS_DERIVED_FROM = "IS_DERIVED_FROM"
    IS_EPOCH_OF = "IS_EPOCH_OF"
    IS_GROUPED_BY = "IS_GROUPED_BY"
    IS_INDICATOR_FOR = "IS_INDICATOR_FOR"
    IS_ORIGINAL_TEXT_FOR = "IS_ORIGINAL_TEXT_FOR"
    IS_POSITION_FOR = "IS_POSITION_FOR"
    IS_REASON_FOR = "IS_REASON_FOR"
    IS_RESULT_OF = "IS_RESULT_OF"
    IS_SPECIMEN_TESTED_IN = "IS_SPECIMEN_TESTED_IN"
    IS_SUBJECT_STATE_FOR = "IS_SUBJECT_STATE_FOR"
    IS_TIMING_FOR = "IS_TIMING_FOR"
    IS_UNIT_FOR = "IS_UNIT_FOR"
    PERFORMED = "PERFORMED"
    PERFORMS = "PERFORMS"
    QUALIFIES = "QUALIFIES"
    SPECIFIES = "SPECIFIES"
    IS_VALUE_OF = "IS_VALUE_OF"
    IS_REFERENCE_TERMINOLOGY_FOR = "IS_REFERENCE_TERMINOLOGY_FOR"


class DataProductLifecycleStatus(str, Enum):
    """
    An enumeration that defines the lifecycle stages for a DataProduct
    """
    Ideation = "Ideation"
    Design = "Design"
    Build = "Build"
    Deploy = "Deploy"
    Consume = "Consume"


class StandardName(str, Enum):
    """
    An enumeration that defines permissible values for standard names
    """
    ADaMIG = "ADaMIG"
    """
    Analysis Data Model Implementation Guide
    """
    BIMO = "BIMO"
    """
    Bioresearch Monitoring
    """
    CDISCSOLIDUSNCI = "CDISC/NCI"
    """
    CDISC/NCI Controlled Terminology
    """
    SDTMIG = "SDTMIG"
    """
    Study Data Tabulation Model Implementation Guide
    """
    SDTMIG_AP = "SDTMIG-AP"
    """
    SDTMIG Associated Persons
    """
    SDTMIG_MD = "SDTMIG-MD"
    """
    SDTMIG Medical Devices
    """
    SENDIG = "SENDIG"
    """
    Standard for Exchange of Non-clinical Data Implementation Guide
    """
    SENDIG_AR = "SENDIG-AR"
    """
    SENDIG Adverse Reactions
    """
    SENDIG_DART = "SENDIG-DART"
    """
    SENDIG Developmental and Reproductive Toxicology
    """
    SENDIG_GENETOX = "SENDIG-GENETOX"
    """
    SENDIG Genetic Toxicology
    """


class StandardType(str, Enum):
    """
    An enumeration that defines permissible values for standard types
    """
    CT = "CT"
    """
    Controlled Terminology
    """
    IG = "IG"
    """
    Implementation Guide
    """


class PublishingSet(str, Enum):
    """
    An enumeration that defines permissible values for publishing sets
    """
    ADaM = "ADaM"
    """
    Analysis Data Model
    """
    CDASH = "CDASH"
    """
    Clinical Data Acquisition Standards Harmonization
    """
    DEFINE_XML = "DEFINE-XML"
    """
    Define-XML Standard
    """
    SDTM = "SDTM"
    """
    Study Data Tabulation Model
    """
    SEND = "SEND"
    """
    Standard for Exchange of Non-clinical Data
    """


class StandardStatus(str, Enum):
    """
    An enumeration that defines permissible values for standard status
    """
    DRAFT = "DRAFT"
    """
    Draft version of the standard
    """
    FINAL = "FINAL"
    """
    Final version of the standard
    """


class LogicalOperator(str, Enum):
    """
    Logical operators for combining conditions in Boolean expressions. For complex expressions, use the EXPRESSION value.
    """
    EXPRESSION = "EXPRESSION"
    """
    Evaluate condition using expression. Default if expression is present.
    """
    AND = "AND"
    """
    All child conditions must be true (all_of). Default if expression is not present.
    """
    OR = "OR"
    """
    At least one child condition must be true (any_of).
    """
    NOT = "NOT"
    """
    Negates the child condition(s) (not_any_of).
    """



class Identifiable(ConfiguredBaseModel):
    """
    A mixin that provides slots for making an entity addressable within a study or context
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://cdisc.org/define-json', 'mixin': True})

    OID: str = Field(default=..., description="""Local identifier within this study/context. Use CDISC OID format for regulatory submissions, or simple strings for internal use.""", json_schema_extra = { "linkml_meta": {'alias': 'OID', 'domain_of': ['Identifiable']} })
    uuid: Optional[str] = Field(default=None, description="""Universal unique identifier""", json_schema_extra = { "linkml_meta": {'alias': 'uuid', 'domain_of': ['Identifiable']} })


class Governed(ConfiguredBaseModel):
    """
    A mixin that provides slots for audit trail and standards governance, including mandatory status, comments, and attribution
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://cdisc.org/define-json',
         'mixin': True,
         'slot_usage': {'OID': {'name': 'OID', 'required': True}}})

    mandatory: Optional[bool] = Field(default=None, description="""Is this element required?""", json_schema_extra = { "linkml_meta": {'alias': 'mandatory', 'domain_of': ['Governed']} })
    comments: Optional[list[str]] = Field(default=None, description="""Comment on the element, such as a rationale for its inclusion or exclusion""", json_schema_extra = { "linkml_meta": {'alias': 'comments', 'domain_of': ['Governed']} })
    siteOrSponsorComments: Optional[list[str]] = Field(default=None, description="""Comment on the element, such as a rationale for its inclusion or exclusion""", json_schema_extra = { "linkml_meta": {'alias': 'siteOrSponsorComments', 'domain_of': ['Governed']} })
    purpose: Optional[Union[TranslatedText, str]] = Field(default=None, description="""Purpose or rationale for this data element""", json_schema_extra = { "linkml_meta": {'alias': 'purpose',
         'any_of': [{'range': 'string'}, {'range': 'TranslatedText'}],
         'domain_of': ['Governed']} })
    lastUpdated: Optional[datetime ] = Field(default=None, description="""When the resource was last updated""", json_schema_extra = { "linkml_meta": {'alias': 'lastUpdated', 'domain_of': ['Governed']} })
    owner: Optional[str] = Field(default=None, description="""Party responsible for this element""", json_schema_extra = { "linkml_meta": {'alias': 'owner',
         'any_of': [{'range': 'User'}, {'range': 'Organization'}, {'range': 'string'}],
         'domain_of': ['Governed'],
         'narrow_mappings': ['prov:wasAttributedTo', 'prov:wasAssociatedBy']} })
    wasDerivedFrom: Optional[str] = Field(default=None, description="""Reference to another item that this item implements or extends, e.g. a template Item definition.""", json_schema_extra = { "linkml_meta": {'alias': 'wasDerivedFrom',
         'any_of': [{'range': 'Item'},
                    {'range': 'ItemGroup'},
                    {'range': 'MetaDataVersion'},
                    {'range': 'CodeList'},
                    {'range': 'ReifiedConcept'},
                    {'range': 'ConceptProperty'},
                    {'range': 'Condition'},
                    {'range': 'Method'},
                    {'range': 'NominalOccurrence'},
                    {'range': 'Dataflow'},
                    {'range': 'CubeComponent'},
                    {'range': 'DataProduct'},
                    {'range': 'ProvisionAgreement'}],
         'domain_of': ['Governed'],
         'exact_mappings': ['prov:wasDerivedFrom']} })


class Labelled(ConfiguredBaseModel):
    """
    A mixin that provides slots for detailing meanings and multilingual descriptions
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://cdisc.org/define-json', 'mixin': True})

    name: Optional[str] = Field(default=None, description="""Short name or identifier, used for field names""", json_schema_extra = { "linkml_meta": {'alias': 'name', 'domain_of': ['Labelled', 'Standard']} })
    description: Optional[Union[TranslatedText, str]] = Field(default=None, description="""Detailed description, shown in tooltips""", json_schema_extra = { "linkml_meta": {'alias': 'description',
         'any_of': [{'range': 'string'}, {'range': 'TranslatedText'}],
         'domain_of': ['Labelled', 'CodeListItem']} })
    coding: Optional[list[Coding]] = Field(default=None, description="""Semantic tags for this element""", json_schema_extra = { "linkml_meta": {'alias': 'coding', 'domain_of': ['Labelled', 'CodeListItem', 'SourceItem']} })
    label: Optional[Union[TranslatedText, str]] = Field(default=None, description="""Human-readable label, shown in UIs""", json_schema_extra = { "linkml_meta": {'alias': 'label',
         'any_of': [{'range': 'string'}, {'range': 'TranslatedText'}],
         'domain_of': ['Labelled'],
         'exact_mappings': ['skos:prefLabel']} })
    aliases: Optional[list[Union[TranslatedText, str]]] = Field(default=None, description="""Alternative name or identifier""", json_schema_extra = { "linkml_meta": {'alias': 'aliases',
         'any_of': [{'range': 'string'}, {'range': 'TranslatedText'}],
         'domain_of': ['Labelled', 'CodeListItem'],
         'exact_mappings': ['skos:altLabel']} })


class IdentifiableElement(Labelled, Identifiable):
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'abstract': True,
         'from_schema': 'https://cdisc.org/define-json',
         'mixins': ['Identifiable', 'Labelled']})

    OID: str = Field(default=..., description="""Local identifier within this study/context. Use CDISC OID format for regulatory submissions, or simple strings for internal use.""", json_schema_extra = { "linkml_meta": {'alias': 'OID', 'domain_of': ['Identifiable']} })
    uuid: Optional[str] = Field(default=None, description="""Universal unique identifier""", json_schema_extra = { "linkml_meta": {'alias': 'uuid', 'domain_of': ['Identifiable']} })
    name: Optional[str] = Field(default=None, description="""Short name or identifier, used for field names""", json_schema_extra = { "linkml_meta": {'alias': 'name', 'domain_of': ['Labelled', 'Standard']} })
    description: Optional[Union[TranslatedText, str]] = Field(default=None, description="""Detailed description, shown in tooltips""", json_schema_extra = { "linkml_meta": {'alias': 'description',
         'any_of': [{'range': 'string'}, {'range': 'TranslatedText'}],
         'domain_of': ['Labelled', 'CodeListItem']} })
    coding: Optional[list[Coding]] = Field(default=None, description="""Semantic tags for this element""", json_schema_extra = { "linkml_meta": {'alias': 'coding', 'domain_of': ['Labelled', 'CodeListItem', 'SourceItem']} })
    label: Optional[Union[TranslatedText, str]] = Field(default=None, description="""Human-readable label, shown in UIs""", json_schema_extra = { "linkml_meta": {'alias': 'label',
         'any_of': [{'range': 'string'}, {'range': 'TranslatedText'}],
         'domain_of': ['Labelled'],
         'exact_mappings': ['skos:prefLabel']} })
    aliases: Optional[list[Union[TranslatedText, str]]] = Field(default=None, description="""Alternative name or identifier""", json_schema_extra = { "linkml_meta": {'alias': 'aliases',
         'any_of': [{'range': 'string'}, {'range': 'TranslatedText'}],
         'domain_of': ['Labelled', 'CodeListItem'],
         'exact_mappings': ['skos:altLabel']} })


class GovernedElement(Labelled, Governed, Identifiable):
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'abstract': True,
         'from_schema': 'https://cdisc.org/define-json',
         'mixins': ['Identifiable', 'Labelled', 'Governed']})

    OID: str = Field(default=..., description="""Local identifier within this study/context. Use CDISC OID format for regulatory submissions, or simple strings for internal use.""", json_schema_extra = { "linkml_meta": {'alias': 'OID', 'domain_of': ['Identifiable']} })
    uuid: Optional[str] = Field(default=None, description="""Universal unique identifier""", json_schema_extra = { "linkml_meta": {'alias': 'uuid', 'domain_of': ['Identifiable']} })
    name: Optional[str] = Field(default=None, description="""Short name or identifier, used for field names""", json_schema_extra = { "linkml_meta": {'alias': 'name', 'domain_of': ['Labelled', 'Standard']} })
    description: Optional[Union[TranslatedText, str]] = Field(default=None, description="""Detailed description, shown in tooltips""", json_schema_extra = { "linkml_meta": {'alias': 'description',
         'any_of': [{'range': 'string'}, {'range': 'TranslatedText'}],
         'domain_of': ['Labelled', 'CodeListItem']} })
    coding: Optional[list[Coding]] = Field(default=None, description="""Semantic tags for this element""", json_schema_extra = { "linkml_meta": {'alias': 'coding', 'domain_of': ['Labelled', 'CodeListItem', 'SourceItem']} })
    label: Optional[Union[TranslatedText, str]] = Field(default=None, description="""Human-readable label, shown in UIs""", json_schema_extra = { "linkml_meta": {'alias': 'label',
         'any_of': [{'range': 'string'}, {'range': 'TranslatedText'}],
         'domain_of': ['Labelled'],
         'exact_mappings': ['skos:prefLabel']} })
    aliases: Optional[list[Union[TranslatedText, str]]] = Field(default=None, description="""Alternative name or identifier""", json_schema_extra = { "linkml_meta": {'alias': 'aliases',
         'any_of': [{'range': 'string'}, {'range': 'TranslatedText'}],
         'domain_of': ['Labelled', 'CodeListItem'],
         'exact_mappings': ['skos:altLabel']} })
    mandatory: Optional[bool] = Field(default=None, description="""Is this element required?""", json_schema_extra = { "linkml_meta": {'alias': 'mandatory', 'domain_of': ['Governed']} })
    comments: Optional[list[str]] = Field(default=None, description="""Comment on the element, such as a rationale for its inclusion or exclusion""", json_schema_extra = { "linkml_meta": {'alias': 'comments', 'domain_of': ['Governed']} })
    siteOrSponsorComments: Optional[list[str]] = Field(default=None, description="""Comment on the element, such as a rationale for its inclusion or exclusion""", json_schema_extra = { "linkml_meta": {'alias': 'siteOrSponsorComments', 'domain_of': ['Governed']} })
    purpose: Optional[Union[TranslatedText, str]] = Field(default=None, description="""Purpose or rationale for this data element""", json_schema_extra = { "linkml_meta": {'alias': 'purpose',
         'any_of': [{'range': 'string'}, {'range': 'TranslatedText'}],
         'domain_of': ['Governed']} })
    lastUpdated: Optional[datetime ] = Field(default=None, description="""When the resource was last updated""", json_schema_extra = { "linkml_meta": {'alias': 'lastUpdated', 'domain_of': ['Governed']} })
    owner: Optional[str] = Field(default=None, description="""Party responsible for this element""", json_schema_extra = { "linkml_meta": {'alias': 'owner',
         'any_of': [{'range': 'User'}, {'range': 'Organization'}, {'range': 'string'}],
         'domain_of': ['Governed'],
         'narrow_mappings': ['prov:wasAttributedTo', 'prov:wasAssociatedBy']} })
    wasDerivedFrom: Optional[str] = Field(default=None, description="""Reference to another item that this item implements or extends, e.g. a template Item definition.""", json_schema_extra = { "linkml_meta": {'alias': 'wasDerivedFrom',
         'any_of': [{'range': 'Item'},
                    {'range': 'ItemGroup'},
                    {'range': 'MetaDataVersion'},
                    {'range': 'CodeList'},
                    {'range': 'ReifiedConcept'},
                    {'range': 'ConceptProperty'},
                    {'range': 'Condition'},
                    {'range': 'Method'},
                    {'range': 'NominalOccurrence'},
                    {'range': 'Dataflow'},
                    {'range': 'CubeComponent'},
                    {'range': 'DataProduct'},
                    {'range': 'ProvisionAgreement'}],
         'domain_of': ['Governed'],
         'exact_mappings': ['prov:wasDerivedFrom']} })


class Formatted(ConfiguredBaseModel):
    """
    A mixin that provides slots for reporting, exchange, or storage formatting
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://cdisc.org/define-json',
         'mixin': True,
         'related_mappings': ['sdmx:Facet', 'sdmx:Representation']})

    decimalDigits: Optional[int] = Field(default=None, description="""For decimal values, the number of digits after the decimal point""", json_schema_extra = { "linkml_meta": {'alias': 'decimalDigits', 'domain_of': ['Formatted']} })
    displayFormat: Optional[str] = Field(default=None, description="""A display format for the item""", json_schema_extra = { "linkml_meta": {'alias': 'displayFormat', 'domain_of': ['Formatted']} })
    significantDigits: Optional[int] = Field(default=None, description="""For numeric values, the number of significant digits""", json_schema_extra = { "linkml_meta": {'alias': 'significantDigits', 'domain_of': ['Formatted']} })


class Versioned(ConfiguredBaseModel):
    """
    A mixin that provides version and connectivity information, including version numbers and resource references
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://cdisc.org/define-json', 'mixin': True})

    version: Optional[str] = Field(default=None, description="""The version of the external resources""", json_schema_extra = { "linkml_meta": {'alias': 'version', 'domain_of': ['Versioned', 'Standard']} })
    href: Optional[str] = Field(default=None, description="""Machine-readable instructions to obtain the resource e.g. FHIR path, URL""", json_schema_extra = { "linkml_meta": {'alias': 'href', 'domain_of': ['Versioned']} })


class IsProfile(Versioned):
    """
    A mixin that provides additional metadata for FHIR resources and Data Products, including profiles, security tags, and validity periods
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://cdisc.org/define-json',
         'mixin': True,
         'mixins': ['Versioned']})

    profile: Optional[list[str]] = Field(default=None, description="""Profiles this resource claims to conform to""", json_schema_extra = { "linkml_meta": {'alias': 'profile', 'domain_of': ['IsProfile']} })
    security: Optional[list[Coding]] = Field(default=None, description="""Security tags applied to this resource""", json_schema_extra = { "linkml_meta": {'alias': 'security', 'domain_of': ['IsProfile']} })
    authenticator: Optional[str] = Field(default=None, description="""Who/what authenticated the resource""", json_schema_extra = { "linkml_meta": {'alias': 'authenticator',
         'any_of': [{'range': 'User'}, {'range': 'Organization'}, {'range': 'string'}],
         'domain_of': ['IsProfile']} })
    validityPeriod: Optional[str] = Field(default=None, description="""Time period during which the resouce is valid""", json_schema_extra = { "linkml_meta": {'alias': 'validityPeriod', 'domain_of': ['IsProfile']} })
    version: Optional[str] = Field(default=None, description="""The version of the external resources""", json_schema_extra = { "linkml_meta": {'alias': 'version', 'domain_of': ['Versioned', 'Standard']} })
    href: Optional[str] = Field(default=None, description="""Machine-readable instructions to obtain the resource e.g. FHIR path, URL""", json_schema_extra = { "linkml_meta": {'alias': 'href', 'domain_of': ['Versioned']} })


class IsODMItem(ConfiguredBaseModel):
    """
    A mixin that provides additional attributes for CDISC Operational Data Model items, including roles, completion instructions, and implementation notes
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://cdisc.org/define-json', 'mixin': True})

    role: Optional[Union[TranslatedText, str]] = Field(default=None, description="""Identifies the role of the item within the containing context, taken from the roleCodeList""", json_schema_extra = { "linkml_meta": {'alias': 'role',
         'any_of': [{'range': 'string'}, {'range': 'TranslatedText'}],
         'domain_of': ['IsODMItem', 'Organization', 'CubeComponent']} })
    roleCodeList: Optional[str] = Field(default=None, description="""Reference to the CodeList that defines the roles for this item""", json_schema_extra = { "linkml_meta": {'alias': 'roleCodeList', 'domain_of': ['IsODMItem']} })
    hasNoData: Optional[bool] = Field(default=None, description="""Set to Yes if this is a manifest and there is no data for this item""", json_schema_extra = { "linkml_meta": {'alias': 'hasNoData', 'domain_of': ['IsODMItem']} })
    crfCompletionInstructions: Optional[Union[TranslatedText, str]] = Field(default=None, description="""CRFCompletionInstructions reference: Instructions for the clinical site on how to enter collected information on the CRF""", json_schema_extra = { "linkml_meta": {'alias': 'crfCompletionInstructions',
         'any_of': [{'range': 'string'}, {'range': 'TranslatedText'}],
         'domain_of': ['IsODMItem']} })
    cdiscNotes: Optional[Union[TranslatedText, str]] = Field(default=None, description="""CDISCNotes reference: Explanatory text for the variable""", json_schema_extra = { "linkml_meta": {'alias': 'cdiscNotes',
         'any_of': [{'range': 'string'}, {'range': 'TranslatedText'}],
         'domain_of': ['IsODMItem']} })
    implementationNotes: Optional[Union[TranslatedText, str]] = Field(default=None, description="""ImplementationNotes reference: Further information, such as rationale and implementation instructions, on how to implement the CRF data collection fields""", json_schema_extra = { "linkml_meta": {'alias': 'implementationNotes',
         'any_of': [{'range': 'string'}, {'range': 'TranslatedText'}],
         'domain_of': ['IsODMItem']} })
    collectionExceptionCondition: Optional[str] = Field(default=None, description="""Condition that defines when collection may be exempted""", json_schema_extra = { "linkml_meta": {'alias': 'collectionExceptionCondition', 'domain_of': ['IsODMItem']} })
    preSpecifiedValue: Optional[Union[TranslatedText, str]] = Field(default=None, description="""Prefill value or a default value for a field that is automatically populated.""", json_schema_extra = { "linkml_meta": {'alias': 'preSpecifiedValue',
         'any_of': [{'range': 'string'}, {'range': 'TranslatedText'}],
         'domain_of': ['IsODMItem']} })


class ODMFileMetadata(ConfiguredBaseModel):
    """
    A mixin that provides ODM file-level metadata attributes including file identifiers, timestamps, and system information
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://cdisc.org/define-json', 'mixin': True})

    fileOID: str = Field(default=..., description="""Unique identifier for the ODM file""", json_schema_extra = { "linkml_meta": {'alias': 'fileOID', 'domain_of': ['ODMFileMetadata']} })
    asOfDateTime: Optional[datetime ] = Field(default=None, description="""Date and time when the data snapshot was taken""", json_schema_extra = { "linkml_meta": {'alias': 'asOfDateTime', 'domain_of': ['ODMFileMetadata']} })
    creationDateTime: datetime  = Field(default=..., description="""Date and time when the ODM file was created""", json_schema_extra = { "linkml_meta": {'alias': 'creationDateTime', 'domain_of': ['ODMFileMetadata']} })
    odmVersion: str = Field(default=..., description="""Version of the ODM standard used""", json_schema_extra = { "linkml_meta": {'alias': 'odmVersion', 'domain_of': ['ODMFileMetadata']} })
    fileType: str = Field(default=..., description="""Type of ODM file (e.g., Snapshot, Transactional)""", json_schema_extra = { "linkml_meta": {'alias': 'fileType', 'domain_of': ['ODMFileMetadata']} })
    originator: Optional[str] = Field(default=None, description="""Organization or system that created the ODM file""", json_schema_extra = { "linkml_meta": {'alias': 'originator', 'domain_of': ['ODMFileMetadata']} })
    sourceSystem: Optional[str] = Field(default=None, description="""Source system that generated the data""", json_schema_extra = { "linkml_meta": {'alias': 'sourceSystem', 'domain_of': ['ODMFileMetadata']} })
    sourceSystemVersion: Optional[str] = Field(default=None, description="""Version of the source system""", json_schema_extra = { "linkml_meta": {'alias': 'sourceSystemVersion', 'domain_of': ['ODMFileMetadata']} })
    context: Optional[str] = Field(default=None, description="""Define-XML context (usually \"Other\" for Define-XML)""", json_schema_extra = { "linkml_meta": {'alias': 'context', 'domain_of': ['ODMFileMetadata', 'FormalExpression']} })
    defineVersion: Optional[str] = Field(default=None, description="""Version of Define-XML specification used""", json_schema_extra = { "linkml_meta": {'alias': 'defineVersion', 'domain_of': ['ODMFileMetadata']} })


class StudyMetadata(ConfiguredBaseModel):
    """
    A mixin that provides study-level metadata attributes including study identification and protocol information
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://cdisc.org/define-json', 'mixin': True})

    studyOID: str = Field(default=..., description="""Unique identifier for the study""", json_schema_extra = { "linkml_meta": {'alias': 'studyOID', 'domain_of': ['StudyMetadata']} })
    studyName: Optional[str] = Field(default=None, description="""Name of the study""", json_schema_extra = { "linkml_meta": {'alias': 'studyName', 'domain_of': ['StudyMetadata']} })
    studyDescription: Optional[str] = Field(default=None, description="""Description of the study""", json_schema_extra = { "linkml_meta": {'alias': 'studyDescription', 'domain_of': ['StudyMetadata']} })
    protocolName: Optional[str] = Field(default=None, description="""Protocol name for the study""", json_schema_extra = { "linkml_meta": {'alias': 'protocolName', 'domain_of': ['StudyMetadata']} })


class MetaDataVersion(StudyMetadata, ODMFileMetadata, GovernedElement):
    """
    A container element that represents a given version of a specification, linking to a particular usage context such as a study, dataset, or data collection instrument.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'close_mappings': ['usdm:StudyDesign'],
         'from_schema': 'https://cdisc.org/define-json',
         'mixins': ['ODMFileMetadata', 'StudyMetadata'],
         'tree_root': True})

    itemGroups: Optional[list[ItemGroup]] = Field(default=None, description="""Item groups, containing items, defined in this version of the metadata""", json_schema_extra = { "linkml_meta": {'alias': 'itemGroups', 'domain_of': ['MetaDataVersion']} })
    items: Optional[list[Item]] = Field(default=None, description="""Template or top-level items (not belonging to any item group) defined in this version of the metadata""", json_schema_extra = { "linkml_meta": {'alias': 'items', 'domain_of': ['MetaDataVersion', 'ItemGroup', 'Parameter']} })
    conditions: Optional[list[Condition]] = Field(default=None, description="""Logical conditions that apply to this version of the metadata.""", json_schema_extra = { "linkml_meta": {'alias': 'conditions',
         'domain_of': ['MetaDataVersion', 'WhereClause', 'Condition', 'Parameter']} })
    whereClauses: Optional[list[WhereClause]] = Field(default=None, description="""Data contexts that apply to this version of the metadata.""", json_schema_extra = { "linkml_meta": {'alias': 'whereClauses', 'domain_of': ['MetaDataVersion']} })
    methods: Optional[list[Method]] = Field(default=None, description="""Methods defined in this version of the metadata.""", json_schema_extra = { "linkml_meta": {'alias': 'methods', 'domain_of': ['MetaDataVersion']} })
    analyses: Optional[list[Analysis]] = Field(default=None, description="""Analyses defined in this version of the metadata.""", json_schema_extra = { "linkml_meta": {'alias': 'analyses', 'domain_of': ['MetaDataVersion']} })
    codeLists: Optional[list[CodeList]] = Field(default=None, description="""Code lists defined in this version of the metadata.""", json_schema_extra = { "linkml_meta": {'alias': 'codeLists', 'domain_of': ['MetaDataVersion']} })
    codings: Optional[list[Coding]] = Field(default=None, description="""Codings defined in this version of the metadata""", json_schema_extra = { "linkml_meta": {'alias': 'codings', 'domain_of': ['MetaDataVersion']} })
    concepts: Optional[list[str]] = Field(default=None, description="""Structured Concepts defined in this version of the metadata""", json_schema_extra = { "linkml_meta": {'alias': 'concepts', 'domain_of': ['MetaDataVersion']} })
    relationships: Optional[list[Relationship]] = Field(default=None, description="""Relationships between items, item groups, and other elements in this version of the metadata.""", json_schema_extra = { "linkml_meta": {'alias': 'relationships', 'domain_of': ['MetaDataVersion']} })
    dictionaries: Optional[list[Dictionary]] = Field(default=None, description="""Dictionaries defined in this version of the metadata""", json_schema_extra = { "linkml_meta": {'alias': 'dictionaries', 'domain_of': ['MetaDataVersion']} })
    standards: Optional[list[Standard]] = Field(default=None, description="""Standards defined in this version of the metadata""", json_schema_extra = { "linkml_meta": {'alias': 'standards', 'domain_of': ['MetaDataVersion']} })
    annotatedCRFs: Optional[list[DocumentReference]] = Field(default=None, description="""Reference to annotated case report forms""", json_schema_extra = { "linkml_meta": {'alias': 'annotatedCRFs', 'domain_of': ['MetaDataVersion']} })
    resources: Optional[list[Union[DocumentReference, Resource]]] = Field(default=None, description="""References to resources and documents that describe this version of the metadata.""", json_schema_extra = { "linkml_meta": {'alias': 'resources',
         'any_of': [{'range': 'DocumentReference'}, {'range': 'Resource'}],
         'domain_of': ['MetaDataVersion']} })
    dataProducts: Optional[list[DataProduct]] = Field(default=None, description="""Indexed data flows with clear ownership""", json_schema_extra = { "linkml_meta": {'alias': 'dataProducts', 'domain_of': ['MetaDataVersion']} })
    displays: Optional[list[Display]] = Field(default=None, description="""Displays defined in this version of the metadata.""", json_schema_extra = { "linkml_meta": {'alias': 'displays', 'domain_of': ['MetaDataVersion']} })
    fileOID: str = Field(default=..., description="""Unique identifier for the ODM file""", json_schema_extra = { "linkml_meta": {'alias': 'fileOID', 'domain_of': ['ODMFileMetadata']} })
    asOfDateTime: Optional[datetime ] = Field(default=None, description="""Date and time when the data snapshot was taken""", json_schema_extra = { "linkml_meta": {'alias': 'asOfDateTime', 'domain_of': ['ODMFileMetadata']} })
    creationDateTime: datetime  = Field(default=..., description="""Date and time when the ODM file was created""", json_schema_extra = { "linkml_meta": {'alias': 'creationDateTime', 'domain_of': ['ODMFileMetadata']} })
    odmVersion: str = Field(default=..., description="""Version of the ODM standard used""", json_schema_extra = { "linkml_meta": {'alias': 'odmVersion', 'domain_of': ['ODMFileMetadata']} })
    fileType: str = Field(default=..., description="""Type of ODM file (e.g., Snapshot, Transactional)""", json_schema_extra = { "linkml_meta": {'alias': 'fileType', 'domain_of': ['ODMFileMetadata']} })
    originator: Optional[str] = Field(default=None, description="""Organization or system that created the ODM file""", json_schema_extra = { "linkml_meta": {'alias': 'originator', 'domain_of': ['ODMFileMetadata']} })
    sourceSystem: Optional[str] = Field(default=None, description="""Source system that generated the data""", json_schema_extra = { "linkml_meta": {'alias': 'sourceSystem', 'domain_of': ['ODMFileMetadata']} })
    sourceSystemVersion: Optional[str] = Field(default=None, description="""Version of the source system""", json_schema_extra = { "linkml_meta": {'alias': 'sourceSystemVersion', 'domain_of': ['ODMFileMetadata']} })
    context: Optional[str] = Field(default=None, description="""Define-XML context (usually \"Other\" for Define-XML)""", json_schema_extra = { "linkml_meta": {'alias': 'context', 'domain_of': ['ODMFileMetadata', 'FormalExpression']} })
    defineVersion: Optional[str] = Field(default=None, description="""Version of Define-XML specification used""", json_schema_extra = { "linkml_meta": {'alias': 'defineVersion', 'domain_of': ['ODMFileMetadata']} })
    studyOID: str = Field(default=..., description="""Unique identifier for the study""", json_schema_extra = { "linkml_meta": {'alias': 'studyOID', 'domain_of': ['StudyMetadata']} })
    studyName: Optional[str] = Field(default=None, description="""Name of the study""", json_schema_extra = { "linkml_meta": {'alias': 'studyName', 'domain_of': ['StudyMetadata']} })
    studyDescription: Optional[str] = Field(default=None, description="""Description of the study""", json_schema_extra = { "linkml_meta": {'alias': 'studyDescription', 'domain_of': ['StudyMetadata']} })
    protocolName: Optional[str] = Field(default=None, description="""Protocol name for the study""", json_schema_extra = { "linkml_meta": {'alias': 'protocolName', 'domain_of': ['StudyMetadata']} })
    OID: str = Field(default=..., description="""Local identifier within this study/context. Use CDISC OID format for regulatory submissions, or simple strings for internal use.""", json_schema_extra = { "linkml_meta": {'alias': 'OID', 'domain_of': ['Identifiable']} })
    uuid: Optional[str] = Field(default=None, description="""Universal unique identifier""", json_schema_extra = { "linkml_meta": {'alias': 'uuid', 'domain_of': ['Identifiable']} })
    name: Optional[str] = Field(default=None, description="""Short name or identifier, used for field names""", json_schema_extra = { "linkml_meta": {'alias': 'name', 'domain_of': ['Labelled', 'Standard']} })
    description: Optional[Union[TranslatedText, str]] = Field(default=None, description="""Detailed description, shown in tooltips""", json_schema_extra = { "linkml_meta": {'alias': 'description',
         'any_of': [{'range': 'string'}, {'range': 'TranslatedText'}],
         'domain_of': ['Labelled', 'CodeListItem']} })
    coding: Optional[list[Coding]] = Field(default=None, description="""Semantic tags for this element""", json_schema_extra = { "linkml_meta": {'alias': 'coding', 'domain_of': ['Labelled', 'CodeListItem', 'SourceItem']} })
    label: Optional[Union[TranslatedText, str]] = Field(default=None, description="""Human-readable label, shown in UIs""", json_schema_extra = { "linkml_meta": {'alias': 'label',
         'any_of': [{'range': 'string'}, {'range': 'TranslatedText'}],
         'domain_of': ['Labelled'],
         'exact_mappings': ['skos:prefLabel']} })
    aliases: Optional[list[Union[TranslatedText, str]]] = Field(default=None, description="""Alternative name or identifier""", json_schema_extra = { "linkml_meta": {'alias': 'aliases',
         'any_of': [{'range': 'string'}, {'range': 'TranslatedText'}],
         'domain_of': ['Labelled', 'CodeListItem'],
         'exact_mappings': ['skos:altLabel']} })
    mandatory: Optional[bool] = Field(default=None, description="""Is this element required?""", json_schema_extra = { "linkml_meta": {'alias': 'mandatory', 'domain_of': ['Governed']} })
    comments: Optional[list[str]] = Field(default=None, description="""Comment on the element, such as a rationale for its inclusion or exclusion""", json_schema_extra = { "linkml_meta": {'alias': 'comments', 'domain_of': ['Governed']} })
    siteOrSponsorComments: Optional[list[str]] = Field(default=None, description="""Comment on the element, such as a rationale for its inclusion or exclusion""", json_schema_extra = { "linkml_meta": {'alias': 'siteOrSponsorComments', 'domain_of': ['Governed']} })
    purpose: Optional[Union[TranslatedText, str]] = Field(default=None, description="""Purpose or rationale for this data element""", json_schema_extra = { "linkml_meta": {'alias': 'purpose',
         'any_of': [{'range': 'string'}, {'range': 'TranslatedText'}],
         'domain_of': ['Governed']} })
    lastUpdated: Optional[datetime ] = Field(default=None, description="""When the resource was last updated""", json_schema_extra = { "linkml_meta": {'alias': 'lastUpdated', 'domain_of': ['Governed']} })
    owner: Optional[str] = Field(default=None, description="""Party responsible for this element""", json_schema_extra = { "linkml_meta": {'alias': 'owner',
         'any_of': [{'range': 'User'}, {'range': 'Organization'}, {'range': 'string'}],
         'domain_of': ['Governed'],
         'narrow_mappings': ['prov:wasAttributedTo', 'prov:wasAssociatedBy']} })
    wasDerivedFrom: Optional[str] = Field(default=None, description="""Reference to another item that this item implements or extends, e.g. a template Item definition.""", json_schema_extra = { "linkml_meta": {'alias': 'wasDerivedFrom',
         'any_of': [{'range': 'Item'},
                    {'range': 'ItemGroup'},
                    {'range': 'MetaDataVersion'},
                    {'range': 'CodeList'},
                    {'range': 'ReifiedConcept'},
                    {'range': 'ConceptProperty'},
                    {'range': 'Condition'},
                    {'range': 'Method'},
                    {'range': 'NominalOccurrence'},
                    {'range': 'Dataflow'},
                    {'range': 'CubeComponent'},
                    {'range': 'DataProduct'},
                    {'range': 'ProvisionAgreement'}],
         'domain_of': ['Governed'],
         'exact_mappings': ['prov:wasDerivedFrom']} })


class Item(IsODMItem, Formatted, GovernedElement):
    """
    A data element that represents a specific piece of information within a defined context, with data type, constraints, and derivation methods
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'close_mappings': ['odm:ItemRef',
                            'odm:ItemDef',
                            'qb:ComponentSpecification',
                            'sdmx:DataAttribute',
                            'sdmx:MetadataAttribute'],
         'from_schema': 'https://cdisc.org/define-json',
         'mixins': ['IsODMItem', 'Formatted'],
         'narrow_mappings': ['fhir:StructureDefinition/variable',
                             'fhir:Questionnaire/item',
                             'qb:ComponentProperty',
                             'omop:Field',
                             'omop:DerivedColumn'],
         'related_mappings': ['usdm:BiomedicalConceptProperty',
                              'usdm:DerivationConceptProperty',
                              'usdm:AnalysisConceptProperty',
                              'fhir:ElementDefinition',
                              'qb:Measure',
                              'qb:Attribute',
                              'sdmx:Concept',
                              'sdmx:Component',
                              'sdmx:Representation',
                              'osb:sdtm_variable',
                              'osb:specimen',
                              'osb:unit_dimension',
                              'osb:std_unit']})

    dataType: DataType = Field(default=..., description="""The data type of the item.""", json_schema_extra = { "linkml_meta": {'alias': 'dataType',
         'domain_of': ['Item', 'CodeList', 'Parameter', 'ReturnValue']} })
    length: Optional[int] = Field(default=None, description="""The maximum length of the data item in characters.""", json_schema_extra = { "linkml_meta": {'alias': 'length', 'domain_of': ['Item']} })
    codeList: Optional[str] = Field(default=None, description="""Reference to the CodeList that constrains the item values.""", json_schema_extra = { "linkml_meta": {'alias': 'codeList', 'domain_of': ['Item', 'ConceptProperty', 'Parameter']} })
    method: Optional[str] = Field(default=None, description="""Reference to the Method element that describes how to derive this item's value.""", json_schema_extra = { "linkml_meta": {'alias': 'method', 'domain_of': ['Item']} })
    rangeChecks: Optional[list[RangeCheck]] = Field(default=None, description="""Range checks applied to this item (e.g. edit checks, CORE rules)""", json_schema_extra = { "linkml_meta": {'alias': 'rangeChecks', 'domain_of': ['Item', 'Condition']} })
    applicableWhen: Optional[list[str]] = Field(default=None, description="""References to different situations that define when this item applies.
Multiple whereClauses are combined with OR logic: the item applies if ANY referenced WhereClause matches.
Within each WhereClause, conditions are combined with AND logic: all conditions must be true.

Example: whereClause: [\"WC.SYSBP\", \"WC.DIABP\"] means the item applies when
(all conditions in WC.SYSBP are true) OR (all conditions in WC.DIABP are true).
""", json_schema_extra = { "linkml_meta": {'alias': 'applicableWhen',
         'close_mappings': ['fhir:StructureDefinition/context'],
         'domain_of': ['Item', 'ItemGroup', 'Parameter', 'Analysis']} })
    origin: Optional[Origin] = Field(default=None, description="""The origin of the data""", json_schema_extra = { "linkml_meta": {'alias': 'origin', 'domain_of': ['Item']} })
    conceptProperty: Optional[str] = Field(default=None, description="""Reference to a abstract concept property that this item is a specialization / instance of.""", json_schema_extra = { "linkml_meta": {'alias': 'conceptProperty', 'domain_of': ['Item', 'Parameter']} })
    role: Optional[Union[TranslatedText, str]] = Field(default=None, description="""Identifies the role of the item within the containing context, taken from the roleCodeList""", json_schema_extra = { "linkml_meta": {'alias': 'role',
         'any_of': [{'range': 'string'}, {'range': 'TranslatedText'}],
         'domain_of': ['IsODMItem', 'Organization', 'CubeComponent']} })
    roleCodeList: Optional[str] = Field(default=None, description="""Reference to the CodeList that defines the roles for this item""", json_schema_extra = { "linkml_meta": {'alias': 'roleCodeList', 'domain_of': ['IsODMItem']} })
    hasNoData: Optional[bool] = Field(default=None, description="""Set to Yes if this is a manifest and there is no data for this item""", json_schema_extra = { "linkml_meta": {'alias': 'hasNoData', 'domain_of': ['IsODMItem']} })
    crfCompletionInstructions: Optional[Union[TranslatedText, str]] = Field(default=None, description="""CRFCompletionInstructions reference: Instructions for the clinical site on how to enter collected information on the CRF""", json_schema_extra = { "linkml_meta": {'alias': 'crfCompletionInstructions',
         'any_of': [{'range': 'string'}, {'range': 'TranslatedText'}],
         'domain_of': ['IsODMItem']} })
    cdiscNotes: Optional[Union[TranslatedText, str]] = Field(default=None, description="""CDISCNotes reference: Explanatory text for the variable""", json_schema_extra = { "linkml_meta": {'alias': 'cdiscNotes',
         'any_of': [{'range': 'string'}, {'range': 'TranslatedText'}],
         'domain_of': ['IsODMItem']} })
    implementationNotes: Optional[Union[TranslatedText, str]] = Field(default=None, description="""ImplementationNotes reference: Further information, such as rationale and implementation instructions, on how to implement the CRF data collection fields""", json_schema_extra = { "linkml_meta": {'alias': 'implementationNotes',
         'any_of': [{'range': 'string'}, {'range': 'TranslatedText'}],
         'domain_of': ['IsODMItem']} })
    collectionExceptionCondition: Optional[str] = Field(default=None, description="""Condition that defines when collection may be exempted""", json_schema_extra = { "linkml_meta": {'alias': 'collectionExceptionCondition', 'domain_of': ['IsODMItem']} })
    preSpecifiedValue: Optional[Union[TranslatedText, str]] = Field(default=None, description="""Prefill value or a default value for a field that is automatically populated.""", json_schema_extra = { "linkml_meta": {'alias': 'preSpecifiedValue',
         'any_of': [{'range': 'string'}, {'range': 'TranslatedText'}],
         'domain_of': ['IsODMItem']} })
    decimalDigits: Optional[int] = Field(default=None, description="""For decimal values, the number of digits after the decimal point""", json_schema_extra = { "linkml_meta": {'alias': 'decimalDigits', 'domain_of': ['Formatted']} })
    displayFormat: Optional[str] = Field(default=None, description="""A display format for the item""", json_schema_extra = { "linkml_meta": {'alias': 'displayFormat', 'domain_of': ['Formatted']} })
    significantDigits: Optional[int] = Field(default=None, description="""For numeric values, the number of significant digits""", json_schema_extra = { "linkml_meta": {'alias': 'significantDigits', 'domain_of': ['Formatted']} })
    OID: str = Field(default=..., description="""Local identifier within this study/context. Use CDISC OID format for regulatory submissions, or simple strings for internal use.""", json_schema_extra = { "linkml_meta": {'alias': 'OID', 'domain_of': ['Identifiable']} })
    uuid: Optional[str] = Field(default=None, description="""Universal unique identifier""", json_schema_extra = { "linkml_meta": {'alias': 'uuid', 'domain_of': ['Identifiable']} })
    name: Optional[str] = Field(default=None, description="""Short name or identifier, used for field names""", json_schema_extra = { "linkml_meta": {'alias': 'name', 'domain_of': ['Labelled', 'Standard']} })
    description: Optional[Union[TranslatedText, str]] = Field(default=None, description="""Detailed description, shown in tooltips""", json_schema_extra = { "linkml_meta": {'alias': 'description',
         'any_of': [{'range': 'string'}, {'range': 'TranslatedText'}],
         'domain_of': ['Labelled', 'CodeListItem']} })
    coding: Optional[list[Coding]] = Field(default=None, description="""Semantic tags for this element""", json_schema_extra = { "linkml_meta": {'alias': 'coding', 'domain_of': ['Labelled', 'CodeListItem', 'SourceItem']} })
    label: Optional[Union[TranslatedText, str]] = Field(default=None, description="""Human-readable label, shown in UIs""", json_schema_extra = { "linkml_meta": {'alias': 'label',
         'any_of': [{'range': 'string'}, {'range': 'TranslatedText'}],
         'domain_of': ['Labelled'],
         'exact_mappings': ['skos:prefLabel']} })
    aliases: Optional[list[Union[TranslatedText, str]]] = Field(default=None, description="""Alternative name or identifier""", json_schema_extra = { "linkml_meta": {'alias': 'aliases',
         'any_of': [{'range': 'string'}, {'range': 'TranslatedText'}],
         'domain_of': ['Labelled', 'CodeListItem'],
         'exact_mappings': ['skos:altLabel']} })
    mandatory: Optional[bool] = Field(default=None, description="""Is this element required?""", json_schema_extra = { "linkml_meta": {'alias': 'mandatory', 'domain_of': ['Governed']} })
    comments: Optional[list[str]] = Field(default=None, description="""Comment on the element, such as a rationale for its inclusion or exclusion""", json_schema_extra = { "linkml_meta": {'alias': 'comments', 'domain_of': ['Governed']} })
    siteOrSponsorComments: Optional[list[str]] = Field(default=None, description="""Comment on the element, such as a rationale for its inclusion or exclusion""", json_schema_extra = { "linkml_meta": {'alias': 'siteOrSponsorComments', 'domain_of': ['Governed']} })
    purpose: Optional[Union[TranslatedText, str]] = Field(default=None, description="""Purpose or rationale for this data element""", json_schema_extra = { "linkml_meta": {'alias': 'purpose',
         'any_of': [{'range': 'string'}, {'range': 'TranslatedText'}],
         'domain_of': ['Governed']} })
    lastUpdated: Optional[datetime ] = Field(default=None, description="""When the resource was last updated""", json_schema_extra = { "linkml_meta": {'alias': 'lastUpdated', 'domain_of': ['Governed']} })
    owner: Optional[str] = Field(default=None, description="""Party responsible for this element""", json_schema_extra = { "linkml_meta": {'alias': 'owner',
         'any_of': [{'range': 'User'}, {'range': 'Organization'}, {'range': 'string'}],
         'domain_of': ['Governed'],
         'narrow_mappings': ['prov:wasAttributedTo', 'prov:wasAssociatedBy']} })
    wasDerivedFrom: Optional[str] = Field(default=None, description="""Reference to another item that this item implements or extends, e.g. a template Item definition.""", json_schema_extra = { "linkml_meta": {'alias': 'wasDerivedFrom',
         'any_of': [{'range': 'Item'},
                    {'range': 'ItemGroup'},
                    {'range': 'MetaDataVersion'},
                    {'range': 'CodeList'},
                    {'range': 'ReifiedConcept'},
                    {'range': 'ConceptProperty'},
                    {'range': 'Condition'},
                    {'range': 'Method'},
                    {'range': 'NominalOccurrence'},
                    {'range': 'Dataflow'},
                    {'range': 'CubeComponent'},
                    {'range': 'DataProduct'},
                    {'range': 'ProvisionAgreement'}],
         'domain_of': ['Governed'],
         'exact_mappings': ['prov:wasDerivedFrom']} })


class ItemGroup(IsProfile, GovernedElement):
    """
    A collection element that groups related items or subgroups within a specific context, used for tables, FHIR resource profiles, biomedical concept specializations, or form sections
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'close_mappings': ['odm:ItemGroupDef',
                            'odm:ItemGroupRef',
                            'osb:ActivityInstance'],
         'from_schema': 'https://cdisc.org/define-json',
         'mixins': ['IsProfile'],
         'narrow_mappings': ['fhir:StructureDefinition',
                             'fhir:ViewDefinition',
                             'fhir:Questionnaire',
                             'omop:Table',
                             'qb:DataStructureDefinition',
                             'sdmx:DataStructureDefinition',
                             'sdmx:MetaDataStructureDefinition'],
         'related_mappings': ['qb:Dataset',
                              'qb:Observation',
                              'qb:ObservationGroup',
                              'qb:Slice',
                              'osb:Activity']})

    domain: Optional[str] = Field(default=None, description="""Domain abbreviation for the dataset.""", json_schema_extra = { "linkml_meta": {'alias': 'domain', 'domain_of': ['ItemGroup', 'DataProduct']} })
    structure: Optional[Union[TranslatedText, str]] = Field(default=None, description="""Data structure of the item group, indicating how the records are organized. If this is a FHIR Resource, is it nested or flattened? If this is a structured concept, is it a Biomedical/Derivation/Analysis concept?""", json_schema_extra = { "linkml_meta": {'alias': 'structure',
         'any_of': [{'range': 'string'}, {'range': 'TranslatedText'}],
         'domain_of': ['ItemGroup', 'Dataflow']} })
    isReferenceData: Optional[bool] = Field(default=None, description="""Set to Yes if this is a reference item group.""", json_schema_extra = { "linkml_meta": {'alias': 'isReferenceData', 'domain_of': ['ItemGroup']} })
    type: Optional[ItemGroupType] = Field(default=None, description="""Type of item group""", json_schema_extra = { "linkml_meta": {'alias': 'type',
         'domain_of': ['ItemGroup',
                       'Method',
                       'Origin',
                       'Organization',
                       'Standard',
                       'Timing']} })
    items: Optional[list[Item]] = Field(default=None, description="""Items in this group""", json_schema_extra = { "linkml_meta": {'alias': 'items',
         'close_mappings': ['fhir:StructureDefinition/snapshot',
                            'fhir:StructureDefinition/differential'],
         'domain_of': ['MetaDataVersion', 'ItemGroup', 'Parameter']} })
    keySequence: Optional[list[str]] = Field(default=None, description="""Ordered list of Items that define the dataset key structure for sorting and uniqueness. Each entry is an OID reference to an Item in the items array. Order determines sorting precedence, merge operations, and record uniqueness. These are allowed to be null, unlike stricter dataset dimensions or primary keys.""", json_schema_extra = { "linkml_meta": {'alias': 'keySequence',
        'close_mappings': ['odm:ItemRef.KeySequence', 'sdmx:DimensionDescriptor'],
        'domain_of': ['ItemGroup']} })
    slices: Optional[list[Union[ItemGroup, str]]] = Field(default=None, description="""Child ItemGroups nested within this item group (e.g., ValueLists under parent domains). Can be either: - Full ItemGroup objects (preferred for hierarchical nesting) - OID string references (for cross-references to avoid duplication)""", json_schema_extra = { "linkml_meta": {'alias': 'slices',
        'any_of': [{'range': 'ItemGroup'}, {'range': 'string'}],
        'domain_of': ['ItemGroup']} })
    implementsConcept: Optional[str] = Field(default=None, description="""Reference to a abstract concept topic that this item group is a specialization of""", json_schema_extra = { "linkml_meta": {'alias': 'implementsConcept', 'domain_of': ['ItemGroup', 'Method']} })
    applicableWhen: Optional[list[str]] = Field(default=None, description="""References to different situations that define when this item applies.
Multiple whereClauses are combined with OR logic: the item applies if ANY referenced WhereClause matches.
Within each WhereClause, conditions are combined with AND logic: all conditions must be true.

Example: whereClause: [\"WC.SYSBP\", \"WC.DIABP\"] means the item applies when
(all conditions in WC.SYSBP are true) OR (all conditions in WC.DIABP are true).
""", json_schema_extra = { "linkml_meta": {'alias': 'applicableWhen',
         'close_mappings': ['fhir:StructureDefinition/context'],
         'domain_of': ['Item', 'ItemGroup', 'Parameter', 'Analysis']} })
    profile: Optional[list[str]] = Field(default=None, description="""Profiles this resource claims to conform to""", json_schema_extra = { "linkml_meta": {'alias': 'profile', 'domain_of': ['IsProfile']} })
    security: Optional[list[Coding]] = Field(default=None, description="""Security tags applied to this resource""", json_schema_extra = { "linkml_meta": {'alias': 'security', 'domain_of': ['IsProfile']} })
    authenticator: Optional[str] = Field(default=None, description="""Who/what authenticated the resource""", json_schema_extra = { "linkml_meta": {'alias': 'authenticator',
         'any_of': [{'range': 'User'}, {'range': 'Organization'}, {'range': 'string'}],
         'domain_of': ['IsProfile']} })
    validityPeriod: Optional[str] = Field(default=None, description="""Time period during which the resouce is valid""", json_schema_extra = { "linkml_meta": {'alias': 'validityPeriod', 'domain_of': ['IsProfile']} })
    OID: str = Field(default=..., description="""Local identifier within this study/context. Use CDISC OID format for regulatory submissions, or simple strings for internal use.""", json_schema_extra = { "linkml_meta": {'alias': 'OID', 'domain_of': ['Identifiable']} })
    uuid: Optional[str] = Field(default=None, description="""Universal unique identifier""", json_schema_extra = { "linkml_meta": {'alias': 'uuid', 'domain_of': ['Identifiable']} })
    name: Optional[str] = Field(default=None, description="""Short name or identifier, used for field names""", json_schema_extra = { "linkml_meta": {'alias': 'name', 'domain_of': ['Labelled', 'Standard']} })
    description: Optional[Union[TranslatedText, str]] = Field(default=None, description="""Detailed description, shown in tooltips""", json_schema_extra = { "linkml_meta": {'alias': 'description',
         'any_of': [{'range': 'string'}, {'range': 'TranslatedText'}],
         'domain_of': ['Labelled', 'CodeListItem']} })
    coding: Optional[list[Coding]] = Field(default=None, description="""Semantic tags for this element""", json_schema_extra = { "linkml_meta": {'alias': 'coding', 'domain_of': ['Labelled', 'CodeListItem', 'SourceItem']} })
    label: Optional[Union[TranslatedText, str]] = Field(default=None, description="""Human-readable label, shown in UIs""", json_schema_extra = { "linkml_meta": {'alias': 'label',
         'any_of': [{'range': 'string'}, {'range': 'TranslatedText'}],
         'domain_of': ['Labelled'],
         'exact_mappings': ['skos:prefLabel']} })
    aliases: Optional[list[Union[TranslatedText, str]]] = Field(default=None, description="""Alternative name or identifier""", json_schema_extra = { "linkml_meta": {'alias': 'aliases',
         'any_of': [{'range': 'string'}, {'range': 'TranslatedText'}],
         'domain_of': ['Labelled', 'CodeListItem'],
         'exact_mappings': ['skos:altLabel']} })
    mandatory: Optional[bool] = Field(default=None, description="""Is this element required?""", json_schema_extra = { "linkml_meta": {'alias': 'mandatory', 'domain_of': ['Governed']} })
    comments: Optional[list[str]] = Field(default=None, description="""Comment on the element, such as a rationale for its inclusion or exclusion""", json_schema_extra = { "linkml_meta": {'alias': 'comments', 'domain_of': ['Governed']} })
    siteOrSponsorComments: Optional[list[str]] = Field(default=None, description="""Comment on the element, such as a rationale for its inclusion or exclusion""", json_schema_extra = { "linkml_meta": {'alias': 'siteOrSponsorComments', 'domain_of': ['Governed']} })
    purpose: Optional[Union[TranslatedText, str]] = Field(default=None, description="""Purpose or rationale for this data element""", json_schema_extra = { "linkml_meta": {'alias': 'purpose',
         'any_of': [{'range': 'string'}, {'range': 'TranslatedText'}],
         'domain_of': ['Governed']} })
    lastUpdated: Optional[datetime ] = Field(default=None, description="""When the resource was last updated""", json_schema_extra = { "linkml_meta": {'alias': 'lastUpdated', 'domain_of': ['Governed']} })
    owner: Optional[str] = Field(default=None, description="""Party responsible for this element""", json_schema_extra = { "linkml_meta": {'alias': 'owner',
         'any_of': [{'range': 'User'}, {'range': 'Organization'}, {'range': 'string'}],
         'domain_of': ['Governed'],
         'narrow_mappings': ['prov:wasAttributedTo', 'prov:wasAssociatedBy']} })
    wasDerivedFrom: Optional[str] = Field(default=None, description="""Reference to another item that this item implements or extends, e.g. a template Item definition.""", json_schema_extra = { "linkml_meta": {'alias': 'wasDerivedFrom',
         'any_of': [{'range': 'Item'},
                    {'range': 'ItemGroup'},
                    {'range': 'MetaDataVersion'},
                    {'range': 'CodeList'},
                    {'range': 'ReifiedConcept'},
                    {'range': 'ConceptProperty'},
                    {'range': 'Condition'},
                    {'range': 'Method'},
                    {'range': 'NominalOccurrence'},
                    {'range': 'Dataflow'},
                    {'range': 'CubeComponent'},
                    {'range': 'DataProduct'},
                    {'range': 'ProvisionAgreement'}],
         'domain_of': ['Governed'],
         'exact_mappings': ['prov:wasDerivedFrom']} })
    version: Optional[str] = Field(default=None, description="""The version of the external resources""", json_schema_extra = { "linkml_meta": {'alias': 'version', 'domain_of': ['Versioned', 'Standard']} })
    href: Optional[str] = Field(default=None, description="""Machine-readable instructions to obtain the resource e.g. FHIR path, URL""", json_schema_extra = { "linkml_meta": {'alias': 'href', 'domain_of': ['Versioned']} })


class Relationship(IdentifiableElement):
    """
    A semantic link that defines connections between elements such as Items or ItemGroups, capturing relationships like \"is the unit for\" or \"assesses seriousness of\"
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://cdisc.org/define-json',
         'related_mappings': ['sdmx:ConceptSchemeMap']})

    subject: str = Field(default=..., description="""The starting element of the relationship (e.g., an Item or ItemGroup).""", json_schema_extra = { "linkml_meta": {'alias': 'subject', 'domain_of': ['Relationship']} })
    object: str = Field(default=..., description="""The ending element of the relationship.""", json_schema_extra = { "linkml_meta": {'alias': 'object', 'domain_of': ['Relationship']} })
    predicateTerm: PredicateTermEnum = Field(default=..., description="""Short variable relationship linking phrase for programming purposes.""", json_schema_extra = { "linkml_meta": {'alias': 'predicateTerm', 'domain_of': ['Relationship']} })
    linkingPhrase: LinkingPhraseEnum = Field(default=..., description="""Variable relationship descriptive linking phrase.""", json_schema_extra = { "linkml_meta": {'alias': 'linkingPhrase', 'domain_of': ['Relationship']} })
    OID: str = Field(default=..., description="""Local identifier within this study/context. Use CDISC OID format for regulatory submissions, or simple strings for internal use.""", json_schema_extra = { "linkml_meta": {'alias': 'OID', 'domain_of': ['Identifiable']} })
    uuid: Optional[str] = Field(default=None, description="""Universal unique identifier""", json_schema_extra = { "linkml_meta": {'alias': 'uuid', 'domain_of': ['Identifiable']} })
    name: Optional[str] = Field(default=None, description="""Short name or identifier, used for field names""", json_schema_extra = { "linkml_meta": {'alias': 'name', 'domain_of': ['Labelled', 'Standard']} })
    description: Optional[Union[TranslatedText, str]] = Field(default=None, description="""Detailed description, shown in tooltips""", json_schema_extra = { "linkml_meta": {'alias': 'description',
         'any_of': [{'range': 'string'}, {'range': 'TranslatedText'}],
         'domain_of': ['Labelled', 'CodeListItem']} })
    coding: Optional[list[Coding]] = Field(default=None, description="""Semantic tags for this element""", json_schema_extra = { "linkml_meta": {'alias': 'coding', 'domain_of': ['Labelled', 'CodeListItem', 'SourceItem']} })
    label: Optional[Union[TranslatedText, str]] = Field(default=None, description="""Human-readable label, shown in UIs""", json_schema_extra = { "linkml_meta": {'alias': 'label',
         'any_of': [{'range': 'string'}, {'range': 'TranslatedText'}],
         'domain_of': ['Labelled'],
         'exact_mappings': ['skos:prefLabel']} })
    aliases: Optional[list[Union[TranslatedText, str]]] = Field(default=None, description="""Alternative name or identifier""", json_schema_extra = { "linkml_meta": {'alias': 'aliases',
         'any_of': [{'range': 'string'}, {'range': 'TranslatedText'}],
         'domain_of': ['Labelled', 'CodeListItem'],
         'exact_mappings': ['skos:altLabel']} })


class Translation(ConfiguredBaseModel):
    """
    A text representation that provides content in a specific language, used for multilingual support
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'exact_mappings': ['odm:TranslatedText', 'sdmx:InternationalString'],
         'from_schema': 'https://cdisc.org/define-json'})

    language: str = Field(default=..., description="""The language of the translation""", json_schema_extra = { "linkml_meta": {'alias': 'language', 'domain_of': ['Translation']} })
    value: str = Field(default=..., description="""The translated text""", json_schema_extra = { "linkml_meta": {'alias': 'value', 'domain_of': ['Translation', 'Parameter', 'Timing']} })


class TranslatedText(ConfiguredBaseModel):
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://cdisc.org/define-json'})

    translations: Optional[list[Translation]] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'translations', 'domain_of': ['TranslatedText']} })


class CodeList(Versioned, GovernedElement):
    """
    A value set that defines a discrete collection of permissible values for an item, corresponding to the ODM CodeList construct
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'close_mappings': ['skos:Collection', 'sdmx:ItemScheme', 'qb:codeList'],
         'exact_mappings': ['odm:CodeList', 'omop:Vocabulary', 'fhir:ValueSet'],
         'from_schema': 'https://cdisc.org/define-json',
         'mixins': ['Versioned'],
         'narrow_mappings': ['sdmx:Codelist', 'sdmx:ValueList', 'sdmx:ConceptScheme'],
         'related_mappings': ['usdm:BiomedicalConceptProperty/responseCodes']})

    dataType: Optional[DataType] = Field(default=None, description="""The data type for the values in the code list""", json_schema_extra = { "linkml_meta": {'alias': 'dataType',
         'domain_of': ['Item', 'CodeList', 'Parameter', 'ReturnValue']} })
    formatName: Optional[str] = Field(default=None, description="""Name of a standard format definition""", json_schema_extra = { "linkml_meta": {'alias': 'formatName', 'domain_of': ['CodeList']} })
    codeListItems: Optional[list[CodeListItem]] = Field(default=None, description="""The individual values that make up this CodeList. The type of CodeListItem included determines its behaviour""", json_schema_extra = { "linkml_meta": {'alias': 'codeListItems', 'domain_of': ['CodeList']} })
    externalCodeList: Optional[str] = Field(default=None, description="""Reference to a code list that is defined externally to this study""", json_schema_extra = { "linkml_meta": {'alias': 'externalCodeList', 'domain_of': ['CodeList']} })
    version: Optional[str] = Field(default=None, description="""The version of the external resources""", json_schema_extra = { "linkml_meta": {'alias': 'version', 'domain_of': ['Versioned', 'Standard']} })
    href: Optional[str] = Field(default=None, description="""Machine-readable instructions to obtain the resource e.g. FHIR path, URL""", json_schema_extra = { "linkml_meta": {'alias': 'href', 'domain_of': ['Versioned']} })
    OID: str = Field(default=..., description="""Local identifier within this study/context. Use CDISC OID format for regulatory submissions, or simple strings for internal use.""", json_schema_extra = { "linkml_meta": {'alias': 'OID', 'domain_of': ['Identifiable']} })
    uuid: Optional[str] = Field(default=None, description="""Universal unique identifier""", json_schema_extra = { "linkml_meta": {'alias': 'uuid', 'domain_of': ['Identifiable']} })
    name: Optional[str] = Field(default=None, description="""Short name or identifier, used for field names""", json_schema_extra = { "linkml_meta": {'alias': 'name', 'domain_of': ['Labelled', 'Standard']} })
    description: Optional[Union[TranslatedText, str]] = Field(default=None, description="""Detailed description, shown in tooltips""", json_schema_extra = { "linkml_meta": {'alias': 'description',
         'any_of': [{'range': 'string'}, {'range': 'TranslatedText'}],
         'domain_of': ['Labelled', 'CodeListItem']} })
    coding: Optional[list[Coding]] = Field(default=None, description="""Semantic tags for this element""", json_schema_extra = { "linkml_meta": {'alias': 'coding', 'domain_of': ['Labelled', 'CodeListItem', 'SourceItem']} })
    label: Optional[Union[TranslatedText, str]] = Field(default=None, description="""Human-readable label, shown in UIs""", json_schema_extra = { "linkml_meta": {'alias': 'label',
         'any_of': [{'range': 'string'}, {'range': 'TranslatedText'}],
         'domain_of': ['Labelled'],
         'exact_mappings': ['skos:prefLabel']} })
    aliases: Optional[list[Union[TranslatedText, str]]] = Field(default=None, description="""Alternative name or identifier""", json_schema_extra = { "linkml_meta": {'alias': 'aliases',
         'any_of': [{'range': 'string'}, {'range': 'TranslatedText'}],
         'domain_of': ['Labelled', 'CodeListItem'],
         'exact_mappings': ['skos:altLabel']} })
    mandatory: Optional[bool] = Field(default=None, description="""Is this element required?""", json_schema_extra = { "linkml_meta": {'alias': 'mandatory', 'domain_of': ['Governed']} })
    comments: Optional[list[str]] = Field(default=None, description="""Comment on the element, such as a rationale for its inclusion or exclusion""", json_schema_extra = { "linkml_meta": {'alias': 'comments', 'domain_of': ['Governed']} })
    siteOrSponsorComments: Optional[list[str]] = Field(default=None, description="""Comment on the element, such as a rationale for its inclusion or exclusion""", json_schema_extra = { "linkml_meta": {'alias': 'siteOrSponsorComments', 'domain_of': ['Governed']} })
    purpose: Optional[Union[TranslatedText, str]] = Field(default=None, description="""Purpose or rationale for this data element""", json_schema_extra = { "linkml_meta": {'alias': 'purpose',
         'any_of': [{'range': 'string'}, {'range': 'TranslatedText'}],
         'domain_of': ['Governed']} })
    lastUpdated: Optional[datetime ] = Field(default=None, description="""When the resource was last updated""", json_schema_extra = { "linkml_meta": {'alias': 'lastUpdated', 'domain_of': ['Governed']} })
    owner: Optional[str] = Field(default=None, description="""Party responsible for this element""", json_schema_extra = { "linkml_meta": {'alias': 'owner',
         'any_of': [{'range': 'User'}, {'range': 'Organization'}, {'range': 'string'}],
         'domain_of': ['Governed'],
         'narrow_mappings': ['prov:wasAttributedTo', 'prov:wasAssociatedBy']} })
    wasDerivedFrom: Optional[str] = Field(default=None, description="""Reference to another item that this item implements or extends, e.g. a template Item definition.""", json_schema_extra = { "linkml_meta": {'alias': 'wasDerivedFrom',
         'any_of': [{'range': 'Item'},
                    {'range': 'ItemGroup'},
                    {'range': 'MetaDataVersion'},
                    {'range': 'CodeList'},
                    {'range': 'ReifiedConcept'},
                    {'range': 'ConceptProperty'},
                    {'range': 'Condition'},
                    {'range': 'Method'},
                    {'range': 'NominalOccurrence'},
                    {'range': 'Dataflow'},
                    {'range': 'CubeComponent'},
                    {'range': 'DataProduct'},
                    {'range': 'ProvisionAgreement'}],
         'domain_of': ['Governed'],
         'exact_mappings': ['prov:wasDerivedFrom']} })


class CodeListItem(ConfiguredBaseModel):
    """
    A structured member of a CodeList that extends the Coding class with additional context-specific properties
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'close_mappings': ['usdm:AliasCode',
                            'usdm:ResponseCode',
                            'fhir:CodeableConcept',
                            'omop:Concept'],
         'exact_mappings': ['odm:CodeListItem'],
         'from_schema': 'https://cdisc.org/define-json',
         'narrow_mappings': ['sdmx:Code', 'sdmx:ValueItem']})

    codedValue: str = Field(default=..., description="""The value of the CodeListItem before decoding""", json_schema_extra = { "linkml_meta": {'alias': 'codedValue', 'domain_of': ['CodeListItem']} })
    decode: Optional[str] = Field(default=None, description="""The decoded value of the CodeListItem""", json_schema_extra = { "linkml_meta": {'alias': 'decode', 'domain_of': ['CodeListItem', 'Coding']} })
    description: Optional[Union[TranslatedText, str]] = Field(default=None, description="""A detailed description of the code (e.g., for documentation purposes)""", json_schema_extra = { "linkml_meta": {'alias': 'description',
         'any_of': [{'range': 'string'}, {'range': 'TranslatedText'}],
         'domain_of': ['Labelled', 'CodeListItem']} })
    coding: Optional[Coding] = Field(default=None, description="""The dictionary definition of the CodeListItem""", json_schema_extra = { "linkml_meta": {'alias': 'coding', 'domain_of': ['Labelled', 'CodeListItem', 'SourceItem']} })
    aliases: Optional[list[Union[TranslatedText, str]]] = Field(default=None, description="""Alternative labels for the code (ODM Alias, skos:altLabel)""", json_schema_extra = { "linkml_meta": {'alias': 'aliases',
         'any_of': [{'range': 'string'}, {'range': 'TranslatedText'}],
         'domain_of': ['Labelled', 'CodeListItem']} })
    weight: Optional[Decimal] = Field(default=None, description="""Numeric significance of the code (e.g., for scoring)""", json_schema_extra = { "linkml_meta": {'alias': 'weight', 'domain_of': ['CodeListItem']} })
    other: Optional[bool] = Field(default=None, description="""Flag to indicate that the term represents \"other\" content""", json_schema_extra = { "linkml_meta": {'alias': 'other', 'domain_of': ['CodeListItem']} })


class Comment(GovernedElement):
    """
    A descriptive element that contains explanatory text provided by a data or metadata handler
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'exact_mappings': ['odm:CommentDef',
                            'usdm:CommentAnnotation',
                            'fhir:Annotation',
                            'sdmx:Annotation'],
         'from_schema': 'https://cdisc.org/define-json'})

    text: Union[TranslatedText, str] = Field(default=..., description="""The comment text.""", json_schema_extra = { "linkml_meta": {'alias': 'text',
         'any_of': [{'range': 'string'}, {'range': 'TranslatedText'}],
         'domain_of': ['Comment', 'SiteOrSponsorComment']} })
    documents: Optional[list[DocumentReference]] = Field(default=None, description="""References to documents that contain or are referenced by this comment""", json_schema_extra = { "linkml_meta": {'alias': 'documents', 'domain_of': ['Comment', 'Method', 'Origin']} })
    OID: str = Field(default=..., description="""Local identifier within this study/context. Use CDISC OID format for regulatory submissions, or simple strings for internal use.""", json_schema_extra = { "linkml_meta": {'alias': 'OID', 'domain_of': ['Identifiable']} })
    uuid: Optional[str] = Field(default=None, description="""Universal unique identifier""", json_schema_extra = { "linkml_meta": {'alias': 'uuid', 'domain_of': ['Identifiable']} })
    name: Optional[str] = Field(default=None, description="""Short name or identifier, used for field names""", json_schema_extra = { "linkml_meta": {'alias': 'name', 'domain_of': ['Labelled', 'Standard']} })
    description: Optional[Union[TranslatedText, str]] = Field(default=None, description="""Detailed description, shown in tooltips""", json_schema_extra = { "linkml_meta": {'alias': 'description',
         'any_of': [{'range': 'string'}, {'range': 'TranslatedText'}],
         'domain_of': ['Labelled', 'CodeListItem']} })
    coding: Optional[list[Coding]] = Field(default=None, description="""Semantic tags for this element""", json_schema_extra = { "linkml_meta": {'alias': 'coding', 'domain_of': ['Labelled', 'CodeListItem', 'SourceItem']} })
    label: Optional[Union[TranslatedText, str]] = Field(default=None, description="""Human-readable label, shown in UIs""", json_schema_extra = { "linkml_meta": {'alias': 'label',
         'any_of': [{'range': 'string'}, {'range': 'TranslatedText'}],
         'domain_of': ['Labelled'],
         'exact_mappings': ['skos:prefLabel']} })
    aliases: Optional[list[Union[TranslatedText, str]]] = Field(default=None, description="""Alternative name or identifier""", json_schema_extra = { "linkml_meta": {'alias': 'aliases',
         'any_of': [{'range': 'string'}, {'range': 'TranslatedText'}],
         'domain_of': ['Labelled', 'CodeListItem'],
         'exact_mappings': ['skos:altLabel']} })
    mandatory: Optional[bool] = Field(default=None, description="""Is this element required?""", json_schema_extra = { "linkml_meta": {'alias': 'mandatory', 'domain_of': ['Governed']} })
    comments: Optional[list[str]] = Field(default=None, description="""Comment on the element, such as a rationale for its inclusion or exclusion""", json_schema_extra = { "linkml_meta": {'alias': 'comments', 'domain_of': ['Governed']} })
    siteOrSponsorComments: Optional[list[str]] = Field(default=None, description="""Comment on the element, such as a rationale for its inclusion or exclusion""", json_schema_extra = { "linkml_meta": {'alias': 'siteOrSponsorComments', 'domain_of': ['Governed']} })
    purpose: Optional[Union[TranslatedText, str]] = Field(default=None, description="""Purpose or rationale for this data element""", json_schema_extra = { "linkml_meta": {'alias': 'purpose',
         'any_of': [{'range': 'string'}, {'range': 'TranslatedText'}],
         'domain_of': ['Governed']} })
    lastUpdated: Optional[datetime ] = Field(default=None, description="""When the resource was last updated""", json_schema_extra = { "linkml_meta": {'alias': 'lastUpdated', 'domain_of': ['Governed']} })
    owner: Optional[str] = Field(default=None, description="""Party responsible for this element""", json_schema_extra = { "linkml_meta": {'alias': 'owner',
         'any_of': [{'range': 'User'}, {'range': 'Organization'}, {'range': 'string'}],
         'domain_of': ['Governed'],
         'narrow_mappings': ['prov:wasAttributedTo', 'prov:wasAssociatedBy']} })
    wasDerivedFrom: Optional[str] = Field(default=None, description="""Reference to another item that this item implements or extends, e.g. a template Item definition.""", json_schema_extra = { "linkml_meta": {'alias': 'wasDerivedFrom',
         'any_of': [{'range': 'Item'},
                    {'range': 'ItemGroup'},
                    {'range': 'MetaDataVersion'},
                    {'range': 'CodeList'},
                    {'range': 'ReifiedConcept'},
                    {'range': 'ConceptProperty'},
                    {'range': 'Condition'},
                    {'range': 'Method'},
                    {'range': 'NominalOccurrence'},
                    {'range': 'Dataflow'},
                    {'range': 'CubeComponent'},
                    {'range': 'DataProduct'},
                    {'range': 'ProvisionAgreement'}],
         'domain_of': ['Governed'],
         'exact_mappings': ['prov:wasDerivedFrom']} })


class Coding(ConfiguredBaseModel):
    """
    A semantic reference that provides standardized codes and their meanings from controlled vocabularies
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'close_mappings': ['omop:Concept',
                            'skos:Concept',
                            'skos:Label',
                            'sdmx:Code',
                            'sdmx:Concept',
                            'sdmx:ISOConceptReference'],
         'exact_mappings': ['odm:Coding', 'usdm:Code', 'fhir:Coding'],
         'from_schema': 'https://cdisc.org/define-json'})

    code: str = Field(default=..., description="""The code value""", json_schema_extra = { "linkml_meta": {'alias': 'code', 'domain_of': ['Coding']} })
    decode: Optional[Union[TranslatedText, str]] = Field(default=None, description="""Human-readable meaning""", json_schema_extra = { "linkml_meta": {'alias': 'decode',
         'any_of': [{'range': 'string'}, {'range': 'TranslatedText'}],
         'domain_of': ['CodeListItem', 'Coding'],
         'exact_mappings': ['skos:prefLabel']} })
    codeSystem: str = Field(default=..., description="""The code system identifier""", json_schema_extra = { "linkml_meta": {'alias': 'codeSystem', 'domain_of': ['Coding']} })
    codeSystemVersion: Optional[str] = Field(default=None, description="""The code system version""", json_schema_extra = { "linkml_meta": {'alias': 'codeSystemVersion', 'domain_of': ['Coding']} })
    aliasType: Optional[AliasPredicate] = Field(default=None, description="""How this coding is related in the context of its parent element""", json_schema_extra = { "linkml_meta": {'alias': 'aliasType', 'domain_of': ['Coding']} })


class Dictionary(Versioned, IdentifiableElement):
    """
    A dictionary that defines a set of codes and their meanings
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://cdisc.org/define-json', 'mixins': ['Versioned']})

    terms: Optional[list[Coding]] = Field(default=None, description="""Terms in this dictionary - leave this empty in most cases to keep the file small""", json_schema_extra = { "linkml_meta": {'alias': 'terms', 'domain_of': ['Dictionary']} })
    publishedBy: Optional[str] = Field(default=None, description="""Associates the Data Provider that reports/publishes the data.""", json_schema_extra = { "linkml_meta": {'alias': 'publishedBy',
         'any_of': [{'range': 'Organization'}, {'range': 'string'}],
         'domain_of': ['Dictionary', 'Dataset']} })
    version: Optional[str] = Field(default=None, description="""The version of the external resources""", json_schema_extra = { "linkml_meta": {'alias': 'version', 'domain_of': ['Versioned', 'Standard']} })
    href: Optional[str] = Field(default=None, description="""Machine-readable instructions to obtain the resource e.g. FHIR path, URL""", json_schema_extra = { "linkml_meta": {'alias': 'href', 'domain_of': ['Versioned']} })
    OID: str = Field(default=..., description="""Local identifier within this study/context. Use CDISC OID format for regulatory submissions, or simple strings for internal use.""", json_schema_extra = { "linkml_meta": {'alias': 'OID', 'domain_of': ['Identifiable']} })
    uuid: Optional[str] = Field(default=None, description="""Universal unique identifier""", json_schema_extra = { "linkml_meta": {'alias': 'uuid', 'domain_of': ['Identifiable']} })
    name: Optional[str] = Field(default=None, description="""Short name or identifier, used for field names""", json_schema_extra = { "linkml_meta": {'alias': 'name', 'domain_of': ['Labelled', 'Standard']} })
    description: Optional[Union[TranslatedText, str]] = Field(default=None, description="""Detailed description, shown in tooltips""", json_schema_extra = { "linkml_meta": {'alias': 'description',
         'any_of': [{'range': 'string'}, {'range': 'TranslatedText'}],
         'domain_of': ['Labelled', 'CodeListItem']} })
    coding: Optional[list[Coding]] = Field(default=None, description="""Semantic tags for this element""", json_schema_extra = { "linkml_meta": {'alias': 'coding', 'domain_of': ['Labelled', 'CodeListItem', 'SourceItem']} })
    label: Optional[Union[TranslatedText, str]] = Field(default=None, description="""Human-readable label, shown in UIs""", json_schema_extra = { "linkml_meta": {'alias': 'label',
         'any_of': [{'range': 'string'}, {'range': 'TranslatedText'}],
         'domain_of': ['Labelled'],
         'exact_mappings': ['skos:prefLabel']} })
    aliases: Optional[list[Union[TranslatedText, str]]] = Field(default=None, description="""Alternative name or identifier""", json_schema_extra = { "linkml_meta": {'alias': 'aliases',
         'any_of': [{'range': 'string'}, {'range': 'TranslatedText'}],
         'domain_of': ['Labelled', 'CodeListItem'],
         'exact_mappings': ['skos:altLabel']} })


class ReifiedConcept(Versioned, GovernedElement):
    """
    A canonical information layer that makes abstract concepts explicit and referenceable, showing how different data implementations represent the same underlying meanings through a star schema structure with multiple properties
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'close_mappings': ['sdmx:MetaDataStructureDefinition',
                            'sdmx:Concept',
                            'osb:Activity'],
         'from_schema': 'https://cdisc.org/define-json',
         'mixins': ['Versioned'],
         'narrow_mappings': ['usdm:BiomedicalConcept',
                             'usdm:AnalysisConcept',
                             'usdm:DerivationConcept'],
         'related_mappings': ['osb:ActivityInstance',
                              'osb:assm_group',
                              'osb:assm_subgroup']})

    properties: Optional[list[ConceptProperty]] = Field(default=None, description="""Properties of the reified object, which can be other governed elements or simple values""", json_schema_extra = { "linkml_meta": {'alias': 'properties', 'domain_of': ['ReifiedConcept']} })
    version: Optional[str] = Field(default=None, description="""The version of the external resources""", json_schema_extra = { "linkml_meta": {'alias': 'version', 'domain_of': ['Versioned', 'Standard']} })
    href: Optional[str] = Field(default=None, description="""Machine-readable instructions to obtain the resource e.g. FHIR path, URL""", json_schema_extra = { "linkml_meta": {'alias': 'href', 'domain_of': ['Versioned']} })
    OID: str = Field(default=..., description="""Local identifier within this study/context. Use CDISC OID format for regulatory submissions, or simple strings for internal use.""", json_schema_extra = { "linkml_meta": {'alias': 'OID', 'domain_of': ['Identifiable']} })
    uuid: Optional[str] = Field(default=None, description="""Universal unique identifier""", json_schema_extra = { "linkml_meta": {'alias': 'uuid', 'domain_of': ['Identifiable']} })
    name: Optional[str] = Field(default=None, description="""Short name or identifier, used for field names""", json_schema_extra = { "linkml_meta": {'alias': 'name', 'domain_of': ['Labelled', 'Standard']} })
    description: Optional[Union[TranslatedText, str]] = Field(default=None, description="""Detailed description, shown in tooltips""", json_schema_extra = { "linkml_meta": {'alias': 'description',
         'any_of': [{'range': 'string'}, {'range': 'TranslatedText'}],
         'domain_of': ['Labelled', 'CodeListItem']} })
    coding: Optional[list[Coding]] = Field(default=None, description="""Semantic tags for this element""", json_schema_extra = { "linkml_meta": {'alias': 'coding', 'domain_of': ['Labelled', 'CodeListItem', 'SourceItem']} })
    label: Optional[Union[TranslatedText, str]] = Field(default=None, description="""Human-readable label, shown in UIs""", json_schema_extra = { "linkml_meta": {'alias': 'label',
         'any_of': [{'range': 'string'}, {'range': 'TranslatedText'}],
         'domain_of': ['Labelled'],
         'exact_mappings': ['skos:prefLabel']} })
    aliases: Optional[list[Union[TranslatedText, str]]] = Field(default=None, description="""Alternative name or identifier""", json_schema_extra = { "linkml_meta": {'alias': 'aliases',
         'any_of': [{'range': 'string'}, {'range': 'TranslatedText'}],
         'domain_of': ['Labelled', 'CodeListItem'],
         'exact_mappings': ['skos:altLabel']} })
    mandatory: Optional[bool] = Field(default=None, description="""Is this element required?""", json_schema_extra = { "linkml_meta": {'alias': 'mandatory', 'domain_of': ['Governed']} })
    comments: Optional[list[str]] = Field(default=None, description="""Comment on the element, such as a rationale for its inclusion or exclusion""", json_schema_extra = { "linkml_meta": {'alias': 'comments', 'domain_of': ['Governed']} })
    siteOrSponsorComments: Optional[list[str]] = Field(default=None, description="""Comment on the element, such as a rationale for its inclusion or exclusion""", json_schema_extra = { "linkml_meta": {'alias': 'siteOrSponsorComments', 'domain_of': ['Governed']} })
    purpose: Optional[Union[TranslatedText, str]] = Field(default=None, description="""Purpose or rationale for this data element""", json_schema_extra = { "linkml_meta": {'alias': 'purpose',
         'any_of': [{'range': 'string'}, {'range': 'TranslatedText'}],
         'domain_of': ['Governed']} })
    lastUpdated: Optional[datetime ] = Field(default=None, description="""When the resource was last updated""", json_schema_extra = { "linkml_meta": {'alias': 'lastUpdated', 'domain_of': ['Governed']} })
    owner: Optional[str] = Field(default=None, description="""Party responsible for this element""", json_schema_extra = { "linkml_meta": {'alias': 'owner',
         'any_of': [{'range': 'User'}, {'range': 'Organization'}, {'range': 'string'}],
         'domain_of': ['Governed'],
         'narrow_mappings': ['prov:wasAttributedTo', 'prov:wasAssociatedBy']} })
    wasDerivedFrom: Optional[str] = Field(default=None, description="""Reference to another item that this item implements or extends, e.g. a template Item definition.""", json_schema_extra = { "linkml_meta": {'alias': 'wasDerivedFrom',
         'any_of': [{'range': 'Item'},
                    {'range': 'ItemGroup'},
                    {'range': 'MetaDataVersion'},
                    {'range': 'CodeList'},
                    {'range': 'ReifiedConcept'},
                    {'range': 'ConceptProperty'},
                    {'range': 'Condition'},
                    {'range': 'Method'},
                    {'range': 'NominalOccurrence'},
                    {'range': 'Dataflow'},
                    {'range': 'CubeComponent'},
                    {'range': 'DataProduct'},
                    {'range': 'ProvisionAgreement'}],
         'domain_of': ['Governed'],
         'exact_mappings': ['prov:wasDerivedFrom']} })


class ConceptProperty(GovernedElement):
    """
    A reified property concept that exists within the context of its containing topic concept
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'close_mappings': ['sdmx:MetaDataAttribute', 'sdmx:Concept'],
         'from_schema': 'https://cdisc.org/define-json',
         'narrow_mappings': ['usdm:BiomedicalConceptProperty',
                             'usdm:DerivationConceptProperty',
                             'usdm:AnalysisConceptProperty'],
         'related_mappings': ['osb:sdtm_variable',
                              'osb:specimen',
                              'osb:unit_dimension',
                              'osb:std_unit',
                              'osb:laterality',
                              'osb:location',
                              'osb:position']})

    minOccurs: Optional[int] = Field(default=None, description="""Minimum number of occurrences of this property in the context. Set to >0 to mandate some number of occurrences""", json_schema_extra = { "linkml_meta": {'alias': 'minOccurs', 'domain_of': ['ConceptProperty']} })
    maxOccurs: Optional[int] = Field(default=None, description="""Maximum number of occurrences of this property in the context. Leave empty for unbounded. Set to 0 to disable property""", json_schema_extra = { "linkml_meta": {'alias': 'maxOccurs', 'domain_of': ['ConceptProperty']} })
    codeList: Optional[str] = Field(default=None, description="""Reference to a CodeList that constrains the values of this property""", json_schema_extra = { "linkml_meta": {'alias': 'codeList', 'domain_of': ['Item', 'ConceptProperty', 'Parameter']} })
    OID: str = Field(default=..., description="""Local identifier within this study/context. Use CDISC OID format for regulatory submissions, or simple strings for internal use.""", json_schema_extra = { "linkml_meta": {'alias': 'OID', 'domain_of': ['Identifiable']} })
    uuid: Optional[str] = Field(default=None, description="""Universal unique identifier""", json_schema_extra = { "linkml_meta": {'alias': 'uuid', 'domain_of': ['Identifiable']} })
    name: Optional[str] = Field(default=None, description="""Short name or identifier, used for field names""", json_schema_extra = { "linkml_meta": {'alias': 'name', 'domain_of': ['Labelled', 'Standard']} })
    description: Optional[Union[TranslatedText, str]] = Field(default=None, description="""Detailed description, shown in tooltips""", json_schema_extra = { "linkml_meta": {'alias': 'description',
         'any_of': [{'range': 'string'}, {'range': 'TranslatedText'}],
         'domain_of': ['Labelled', 'CodeListItem']} })
    coding: Optional[list[Coding]] = Field(default=None, description="""Semantic tags for this element""", json_schema_extra = { "linkml_meta": {'alias': 'coding', 'domain_of': ['Labelled', 'CodeListItem', 'SourceItem']} })
    label: Optional[Union[TranslatedText, str]] = Field(default=None, description="""Human-readable label, shown in UIs""", json_schema_extra = { "linkml_meta": {'alias': 'label',
         'any_of': [{'range': 'string'}, {'range': 'TranslatedText'}],
         'domain_of': ['Labelled'],
         'exact_mappings': ['skos:prefLabel']} })
    aliases: Optional[list[Union[TranslatedText, str]]] = Field(default=None, description="""Alternative name or identifier""", json_schema_extra = { "linkml_meta": {'alias': 'aliases',
         'any_of': [{'range': 'string'}, {'range': 'TranslatedText'}],
         'domain_of': ['Labelled', 'CodeListItem'],
         'exact_mappings': ['skos:altLabel']} })
    mandatory: Optional[bool] = Field(default=None, description="""Is this element required?""", json_schema_extra = { "linkml_meta": {'alias': 'mandatory', 'domain_of': ['Governed']} })
    comments: Optional[list[str]] = Field(default=None, description="""Comment on the element, such as a rationale for its inclusion or exclusion""", json_schema_extra = { "linkml_meta": {'alias': 'comments', 'domain_of': ['Governed']} })
    siteOrSponsorComments: Optional[list[str]] = Field(default=None, description="""Comment on the element, such as a rationale for its inclusion or exclusion""", json_schema_extra = { "linkml_meta": {'alias': 'siteOrSponsorComments', 'domain_of': ['Governed']} })
    purpose: Optional[Union[TranslatedText, str]] = Field(default=None, description="""Purpose or rationale for this data element""", json_schema_extra = { "linkml_meta": {'alias': 'purpose',
         'any_of': [{'range': 'string'}, {'range': 'TranslatedText'}],
         'domain_of': ['Governed']} })
    lastUpdated: Optional[datetime ] = Field(default=None, description="""When the resource was last updated""", json_schema_extra = { "linkml_meta": {'alias': 'lastUpdated', 'domain_of': ['Governed']} })
    owner: Optional[str] = Field(default=None, description="""Party responsible for this element""", json_schema_extra = { "linkml_meta": {'alias': 'owner',
         'any_of': [{'range': 'User'}, {'range': 'Organization'}, {'range': 'string'}],
         'domain_of': ['Governed'],
         'narrow_mappings': ['prov:wasAttributedTo', 'prov:wasAssociatedBy']} })
    wasDerivedFrom: Optional[str] = Field(default=None, description="""Reference to another item that this item implements or extends, e.g. a template Item definition.""", json_schema_extra = { "linkml_meta": {'alias': 'wasDerivedFrom',
         'any_of': [{'range': 'Item'},
                    {'range': 'ItemGroup'},
                    {'range': 'MetaDataVersion'},
                    {'range': 'CodeList'},
                    {'range': 'ReifiedConcept'},
                    {'range': 'ConceptProperty'},
                    {'range': 'Condition'},
                    {'range': 'Method'},
                    {'range': 'NominalOccurrence'},
                    {'range': 'Dataflow'},
                    {'range': 'CubeComponent'},
                    {'range': 'DataProduct'},
                    {'range': 'ProvisionAgreement'}],
         'domain_of': ['Governed'],
         'exact_mappings': ['prov:wasDerivedFrom']} })


class WhereClause(GovernedElement):
    """
    A conditional element that describes the circumstances under which a containing context applies, linking conditions to structures where they are used
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'close_mappings': ['sdmx:AttachmentConstraint'],
         'from_schema': 'https://cdisc.org/define-json',
         'related_mappings': ['fhir:StructureDefinition/context',
                              'qb:ObservationGroup',
                              'qb:Slice',
                              'sdmx:CubeRegion',
                              'sdmx:MetadataTargetRegion']})

    conditions: Optional[list[str]] = Field(default=None, description="""Logical conditions that apply in this context (combined with AND)""", json_schema_extra = { "linkml_meta": {'alias': 'conditions',
         'domain_of': ['MetaDataVersion', 'WhereClause', 'Condition', 'Parameter']} })
    OID: str = Field(default=..., description="""Local identifier within this study/context. Use CDISC OID format for regulatory submissions, or simple strings for internal use.""", json_schema_extra = { "linkml_meta": {'alias': 'OID', 'domain_of': ['Identifiable']} })
    uuid: Optional[str] = Field(default=None, description="""Universal unique identifier""", json_schema_extra = { "linkml_meta": {'alias': 'uuid', 'domain_of': ['Identifiable']} })
    name: Optional[str] = Field(default=None, description="""Short name or identifier, used for field names""", json_schema_extra = { "linkml_meta": {'alias': 'name', 'domain_of': ['Labelled', 'Standard']} })
    description: Optional[Union[TranslatedText, str]] = Field(default=None, description="""Detailed description, shown in tooltips""", json_schema_extra = { "linkml_meta": {'alias': 'description',
         'any_of': [{'range': 'string'}, {'range': 'TranslatedText'}],
         'domain_of': ['Labelled', 'CodeListItem']} })
    coding: Optional[list[Coding]] = Field(default=None, description="""Semantic tags for this element""", json_schema_extra = { "linkml_meta": {'alias': 'coding', 'domain_of': ['Labelled', 'CodeListItem', 'SourceItem']} })
    label: Optional[Union[TranslatedText, str]] = Field(default=None, description="""Human-readable label, shown in UIs""", json_schema_extra = { "linkml_meta": {'alias': 'label',
         'any_of': [{'range': 'string'}, {'range': 'TranslatedText'}],
         'domain_of': ['Labelled'],
         'exact_mappings': ['skos:prefLabel']} })
    aliases: Optional[list[Union[TranslatedText, str]]] = Field(default=None, description="""Alternative name or identifier""", json_schema_extra = { "linkml_meta": {'alias': 'aliases',
         'any_of': [{'range': 'string'}, {'range': 'TranslatedText'}],
         'domain_of': ['Labelled', 'CodeListItem'],
         'exact_mappings': ['skos:altLabel']} })
    mandatory: Optional[bool] = Field(default=None, description="""Is this element required?""", json_schema_extra = { "linkml_meta": {'alias': 'mandatory', 'domain_of': ['Governed']} })
    comments: Optional[list[str]] = Field(default=None, description="""Comment on the element, such as a rationale for its inclusion or exclusion""", json_schema_extra = { "linkml_meta": {'alias': 'comments', 'domain_of': ['Governed']} })
    siteOrSponsorComments: Optional[list[str]] = Field(default=None, description="""Comment on the element, such as a rationale for its inclusion or exclusion""", json_schema_extra = { "linkml_meta": {'alias': 'siteOrSponsorComments', 'domain_of': ['Governed']} })
    purpose: Optional[Union[TranslatedText, str]] = Field(default=None, description="""Purpose or rationale for this data element""", json_schema_extra = { "linkml_meta": {'alias': 'purpose',
         'any_of': [{'range': 'string'}, {'range': 'TranslatedText'}],
         'domain_of': ['Governed']} })
    lastUpdated: Optional[datetime ] = Field(default=None, description="""When the resource was last updated""", json_schema_extra = { "linkml_meta": {'alias': 'lastUpdated', 'domain_of': ['Governed']} })
    owner: Optional[str] = Field(default=None, description="""Party responsible for this element""", json_schema_extra = { "linkml_meta": {'alias': 'owner',
         'any_of': [{'range': 'User'}, {'range': 'Organization'}, {'range': 'string'}],
         'domain_of': ['Governed'],
         'narrow_mappings': ['prov:wasAttributedTo', 'prov:wasAssociatedBy']} })
    wasDerivedFrom: Optional[str] = Field(default=None, description="""Reference to another item that this item implements or extends, e.g. a template Item definition.""", json_schema_extra = { "linkml_meta": {'alias': 'wasDerivedFrom',
         'any_of': [{'range': 'Item'},
                    {'range': 'ItemGroup'},
                    {'range': 'MetaDataVersion'},
                    {'range': 'CodeList'},
                    {'range': 'ReifiedConcept'},
                    {'range': 'ConceptProperty'},
                    {'range': 'Condition'},
                    {'range': 'Method'},
                    {'range': 'NominalOccurrence'},
                    {'range': 'Dataflow'},
                    {'range': 'CubeComponent'},
                    {'range': 'DataProduct'},
                    {'range': 'ProvisionAgreement'}],
         'domain_of': ['Governed'],
         'exact_mappings': ['prov:wasDerivedFrom']} })


class Condition(GovernedElement):
    """
    A reusable, composable, and nestable logical construct allowing for complex expressions. Conditions are most useful when given a meaningful name and linked to Study Definitions.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'close_mappings': ['odm:ConditionDef', 'usdm:Condition'],
         'from_schema': 'https://cdisc.org/define-json',
         'related_mappings': ['fhir:Expression',
                              'qb:SliceKey',
                              'sdmx:DataConstraint',
                              'sdmx:MetaDataConstraint',
                              'sdmx:DataKeySet']})

    rangeChecks: Optional[list[RangeCheck]] = Field(default=None, description="""Range checks that compose this condition""", json_schema_extra = { "linkml_meta": {'alias': 'rangeChecks', 'domain_of': ['Item', 'Condition']} })
    implementsCondition: Optional[str] = Field(default=None, description="""Reference to a external (e.g. USDM) condition definition that this implements""", json_schema_extra = { "linkml_meta": {'alias': 'implementsCondition', 'domain_of': ['Condition']} })
    expressions: Optional[list[FormalExpression]] = Field(default=None, description="""Logical expression, resolving to a boolean, that implements this condition in a specific context""", json_schema_extra = { "linkml_meta": {'alias': 'expressions', 'domain_of': ['Condition', 'RangeCheck', 'Method']} })
    operator: Optional[LogicalOperator] = Field(default=None, description="""Logical operator for combining child conditions or range checks. Defaults to ALL if not specified.""", json_schema_extra = { "linkml_meta": {'alias': 'operator', 'domain_of': ['Condition', 'RangeCheck']} })
    conditions: Optional[list[str]] = Field(default=None, description="""Child conditions to combine using the operator. Multiple conditions are composed according to the operator (AND/OR/NOT). Rearrange and nest to compose XOR, or combinations of AND and OR. Unless the operator is EXPRESSION, in which case the formalExpression is used instead. Use OID references to reuse conditions defined elsewhere.""", json_schema_extra = { "linkml_meta": {'alias': 'conditions',
         'domain_of': ['MetaDataVersion', 'WhereClause', 'Condition', 'Parameter']} })
    OID: str = Field(default=..., description="""Local identifier within this study/context. Use CDISC OID format for regulatory submissions, or simple strings for internal use.""", json_schema_extra = { "linkml_meta": {'alias': 'OID', 'domain_of': ['Identifiable']} })
    uuid: Optional[str] = Field(default=None, description="""Universal unique identifier""", json_schema_extra = { "linkml_meta": {'alias': 'uuid', 'domain_of': ['Identifiable']} })
    name: Optional[str] = Field(default=None, description="""Short name or identifier, used for field names""", json_schema_extra = { "linkml_meta": {'alias': 'name', 'domain_of': ['Labelled', 'Standard']} })
    description: Optional[Union[TranslatedText, str]] = Field(default=None, description="""Detailed description, shown in tooltips""", json_schema_extra = { "linkml_meta": {'alias': 'description',
         'any_of': [{'range': 'string'}, {'range': 'TranslatedText'}],
         'domain_of': ['Labelled', 'CodeListItem']} })
    coding: Optional[list[Coding]] = Field(default=None, description="""Semantic tags for this element""", json_schema_extra = { "linkml_meta": {'alias': 'coding', 'domain_of': ['Labelled', 'CodeListItem', 'SourceItem']} })
    label: Optional[Union[TranslatedText, str]] = Field(default=None, description="""Human-readable label, shown in UIs""", json_schema_extra = { "linkml_meta": {'alias': 'label',
         'any_of': [{'range': 'string'}, {'range': 'TranslatedText'}],
         'domain_of': ['Labelled'],
         'exact_mappings': ['skos:prefLabel']} })
    aliases: Optional[list[Union[TranslatedText, str]]] = Field(default=None, description="""Alternative name or identifier""", json_schema_extra = { "linkml_meta": {'alias': 'aliases',
         'any_of': [{'range': 'string'}, {'range': 'TranslatedText'}],
         'domain_of': ['Labelled', 'CodeListItem'],
         'exact_mappings': ['skos:altLabel']} })
    mandatory: Optional[bool] = Field(default=None, description="""Is this element required?""", json_schema_extra = { "linkml_meta": {'alias': 'mandatory', 'domain_of': ['Governed']} })
    comments: Optional[list[str]] = Field(default=None, description="""Comment on the element, such as a rationale for its inclusion or exclusion""", json_schema_extra = { "linkml_meta": {'alias': 'comments', 'domain_of': ['Governed']} })
    siteOrSponsorComments: Optional[list[str]] = Field(default=None, description="""Comment on the element, such as a rationale for its inclusion or exclusion""", json_schema_extra = { "linkml_meta": {'alias': 'siteOrSponsorComments', 'domain_of': ['Governed']} })
    purpose: Optional[Union[TranslatedText, str]] = Field(default=None, description="""Purpose or rationale for this data element""", json_schema_extra = { "linkml_meta": {'alias': 'purpose',
         'any_of': [{'range': 'string'}, {'range': 'TranslatedText'}],
         'domain_of': ['Governed']} })
    lastUpdated: Optional[datetime ] = Field(default=None, description="""When the resource was last updated""", json_schema_extra = { "linkml_meta": {'alias': 'lastUpdated', 'domain_of': ['Governed']} })
    owner: Optional[str] = Field(default=None, description="""Party responsible for this element""", json_schema_extra = { "linkml_meta": {'alias': 'owner',
         'any_of': [{'range': 'User'}, {'range': 'Organization'}, {'range': 'string'}],
         'domain_of': ['Governed'],
         'narrow_mappings': ['prov:wasAttributedTo', 'prov:wasAssociatedBy']} })
    wasDerivedFrom: Optional[str] = Field(default=None, description="""Reference to another item that this item implements or extends, e.g. a template Item definition.""", json_schema_extra = { "linkml_meta": {'alias': 'wasDerivedFrom',
         'any_of': [{'range': 'Item'},
                    {'range': 'ItemGroup'},
                    {'range': 'MetaDataVersion'},
                    {'range': 'CodeList'},
                    {'range': 'ReifiedConcept'},
                    {'range': 'ConceptProperty'},
                    {'range': 'Condition'},
                    {'range': 'Method'},
                    {'range': 'NominalOccurrence'},
                    {'range': 'Dataflow'},
                    {'range': 'CubeComponent'},
                    {'range': 'DataProduct'},
                    {'range': 'ProvisionAgreement'}],
         'domain_of': ['Governed'],
         'exact_mappings': ['prov:wasDerivedFrom']} })


class RangeCheck(ConfiguredBaseModel):
    """
    A validation element that performs a simple comparison check between a referenced item's value and specified values, resolving to a boolean result
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://cdisc.org/define-json',
         'related_mappings': ['qb:SliceKey', 'sdmx:DataKey']})

    comparator: Optional[Comparator] = Field(default=None, description="""The type of comparison to be performed""", json_schema_extra = { "linkml_meta": {'alias': 'comparator', 'domain_of': ['RangeCheck']} })
    checkValues: Optional[list[str]] = Field(default=None, description="""Values to compare against""", json_schema_extra = { "linkml_meta": {'alias': 'checkValues', 'domain_of': ['RangeCheck']} })
    item: Optional[str] = Field(default=None, description="""Reference to the Item element whose value is being checked. If not specified, check applies to the enclosing context""", json_schema_extra = { "linkml_meta": {'alias': 'item',
         'any_of': [{'range': 'Item'},
                    {'range': 'Dimension'},
                    {'range': 'Measure'},
                    {'range': 'DataAttribute'}],
         'domain_of': ['RangeCheck',
                       'SourceItem',
                       'CubeComponent',
                       'ObservationRelationship']} })
    softHard: Optional[SoftHard] = Field(default=None, description="""Indicates whether a validation check is an error (\"Hard\") or a warning (\"Soft\")""", json_schema_extra = { "linkml_meta": {'alias': 'softHard', 'domain_of': ['RangeCheck']} })
    expressions: Optional[list[FormalExpression]] = Field(default=None, description="""A formal expression for complex checks""", json_schema_extra = { "linkml_meta": {'alias': 'expressions', 'domain_of': ['Condition', 'RangeCheck', 'Method']} })
    operator: Optional[LogicalOperator] = Field(default=None, description="""Logical operator for combining child conditions or range checks. Defaults to ALL if not specified.""", json_schema_extra = { "linkml_meta": {'alias': 'operator', 'domain_of': ['Condition', 'RangeCheck']} })


class FormalExpression(IdentifiableElement):
    """
    A computational element that defines the execution of a data derivation within a specific context
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'exact_mappings': ['odm:FormalExpression',
                            'odm:FormalExpressionRef',
                            'fhir:Expression'],
         'from_schema': 'https://cdisc.org/define-json'})

    context: Optional[str] = Field(default=None, description="""The specific context within the containing element to which this formal expression applies.""", json_schema_extra = { "linkml_meta": {'alias': 'context',
         'domain_of': ['ODMFileMetadata', 'FormalExpression'],
         'exact_mappings': ['fhir:Expression/language']} })
    expression: str = Field(default=..., description="""The actual text of the formal expression (renamed from 'code' for disambiguation).""", json_schema_extra = { "linkml_meta": {'alias': 'expression', 'aliases': ['code'], 'domain_of': ['FormalExpression']} })
    returnType: Optional[str] = Field(default=None, description="""Return type of the expression""", json_schema_extra = { "linkml_meta": {'alias': 'returnType', 'domain_of': ['FormalExpression']} })
    parameters: Optional[list[Parameter]] = Field(default=None, description="""Parameters used in the expression""", json_schema_extra = { "linkml_meta": {'alias': 'parameters', 'domain_of': ['FormalExpression']} })
    returnValue: Optional[str] = Field(default=None, description="""Return value details""", json_schema_extra = { "linkml_meta": {'alias': 'returnValue', 'domain_of': ['FormalExpression']} })
    externalCodeLibs: Optional[list[str]] = Field(default=None, description="""External code libraries referenced""", json_schema_extra = { "linkml_meta": {'alias': 'externalCodeLibs', 'domain_of': ['FormalExpression']} })
    OID: str = Field(default=..., description="""Local identifier within this study/context. Use CDISC OID format for regulatory submissions, or simple strings for internal use.""", json_schema_extra = { "linkml_meta": {'alias': 'OID', 'domain_of': ['Identifiable']} })
    uuid: Optional[str] = Field(default=None, description="""Universal unique identifier""", json_schema_extra = { "linkml_meta": {'alias': 'uuid', 'domain_of': ['Identifiable']} })
    name: Optional[str] = Field(default=None, description="""Short name or identifier, used for field names""", json_schema_extra = { "linkml_meta": {'alias': 'name', 'domain_of': ['Labelled', 'Standard']} })
    description: Optional[Union[TranslatedText, str]] = Field(default=None, description="""Detailed description, shown in tooltips""", json_schema_extra = { "linkml_meta": {'alias': 'description',
         'any_of': [{'range': 'string'}, {'range': 'TranslatedText'}],
         'domain_of': ['Labelled', 'CodeListItem']} })
    coding: Optional[list[Coding]] = Field(default=None, description="""Semantic tags for this element""", json_schema_extra = { "linkml_meta": {'alias': 'coding', 'domain_of': ['Labelled', 'CodeListItem', 'SourceItem']} })
    label: Optional[Union[TranslatedText, str]] = Field(default=None, description="""Human-readable label, shown in UIs""", json_schema_extra = { "linkml_meta": {'alias': 'label',
         'any_of': [{'range': 'string'}, {'range': 'TranslatedText'}],
         'domain_of': ['Labelled'],
         'exact_mappings': ['skos:prefLabel']} })
    aliases: Optional[list[Union[TranslatedText, str]]] = Field(default=None, description="""Alternative name or identifier""", json_schema_extra = { "linkml_meta": {'alias': 'aliases',
         'any_of': [{'range': 'string'}, {'range': 'TranslatedText'}],
         'domain_of': ['Labelled', 'CodeListItem'],
         'exact_mappings': ['skos:altLabel']} })


class Method(GovernedElement):
    """
    A reusable computational procedure that describes how to derive values and can be referenced by Items.
    Analysis and Derivation concepts can be implemented by a Method. Properties can be referenced by Parameters in its expressions.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'close_mappings': ['fhir:Expression', 'omop:Transformation'],
         'exact_mappings': ['odm:MethodRef', 'odm:MethodDef'],
         'from_schema': 'https://cdisc.org/define-json'})

    type: Optional[MethodType] = Field(default=None, description="""The type of method e.g. Computation, Imputation, Transformation.""", json_schema_extra = { "linkml_meta": {'alias': 'type',
         'domain_of': ['ItemGroup',
                       'Method',
                       'Origin',
                       'Organization',
                       'Standard',
                       'Timing']} })
    expressions: Optional[list[FormalExpression]] = Field(default=None, description="""Formal expressions used by this method""", json_schema_extra = { "linkml_meta": {'alias': 'expressions', 'domain_of': ['Condition', 'RangeCheck', 'Method']} })
    documents: Optional[list[DocumentReference]] = Field(default=None, description="""Reference to a document that describes this method in detail.""", json_schema_extra = { "linkml_meta": {'alias': 'documents', 'domain_of': ['Comment', 'Method', 'Origin']} })
    implementsConcept: Optional[str] = Field(default=None, description="""Reference to a specific concept that this Method implements.""", json_schema_extra = { "linkml_meta": {'alias': 'implementsConcept', 'domain_of': ['ItemGroup', 'Method']} })
    OID: str = Field(default=..., description="""Local identifier within this study/context. Use CDISC OID format for regulatory submissions, or simple strings for internal use.""", json_schema_extra = { "linkml_meta": {'alias': 'OID', 'domain_of': ['Identifiable']} })
    uuid: Optional[str] = Field(default=None, description="""Universal unique identifier""", json_schema_extra = { "linkml_meta": {'alias': 'uuid', 'domain_of': ['Identifiable']} })
    name: Optional[str] = Field(default=None, description="""Short name or identifier, used for field names""", json_schema_extra = { "linkml_meta": {'alias': 'name', 'domain_of': ['Labelled', 'Standard']} })
    description: Optional[Union[TranslatedText, str]] = Field(default=None, description="""Detailed description, shown in tooltips""", json_schema_extra = { "linkml_meta": {'alias': 'description',
         'any_of': [{'range': 'string'}, {'range': 'TranslatedText'}],
         'domain_of': ['Labelled', 'CodeListItem']} })
    coding: Optional[list[Coding]] = Field(default=None, description="""Semantic tags for this element""", json_schema_extra = { "linkml_meta": {'alias': 'coding', 'domain_of': ['Labelled', 'CodeListItem', 'SourceItem']} })
    label: Optional[Union[TranslatedText, str]] = Field(default=None, description="""Human-readable label, shown in UIs""", json_schema_extra = { "linkml_meta": {'alias': 'label',
         'any_of': [{'range': 'string'}, {'range': 'TranslatedText'}],
         'domain_of': ['Labelled'],
         'exact_mappings': ['skos:prefLabel']} })
    aliases: Optional[list[Union[TranslatedText, str]]] = Field(default=None, description="""Alternative name or identifier""", json_schema_extra = { "linkml_meta": {'alias': 'aliases',
         'any_of': [{'range': 'string'}, {'range': 'TranslatedText'}],
         'domain_of': ['Labelled', 'CodeListItem'],
         'exact_mappings': ['skos:altLabel']} })
    mandatory: Optional[bool] = Field(default=None, description="""Is this element required?""", json_schema_extra = { "linkml_meta": {'alias': 'mandatory', 'domain_of': ['Governed']} })
    comments: Optional[list[str]] = Field(default=None, description="""Comment on the element, such as a rationale for its inclusion or exclusion""", json_schema_extra = { "linkml_meta": {'alias': 'comments', 'domain_of': ['Governed']} })
    siteOrSponsorComments: Optional[list[str]] = Field(default=None, description="""Comment on the element, such as a rationale for its inclusion or exclusion""", json_schema_extra = { "linkml_meta": {'alias': 'siteOrSponsorComments', 'domain_of': ['Governed']} })
    purpose: Optional[Union[TranslatedText, str]] = Field(default=None, description="""Purpose or rationale for this data element""", json_schema_extra = { "linkml_meta": {'alias': 'purpose',
         'any_of': [{'range': 'string'}, {'range': 'TranslatedText'}],
         'domain_of': ['Governed']} })
    lastUpdated: Optional[datetime ] = Field(default=None, description="""When the resource was last updated""", json_schema_extra = { "linkml_meta": {'alias': 'lastUpdated', 'domain_of': ['Governed']} })
    owner: Optional[str] = Field(default=None, description="""Party responsible for this element""", json_schema_extra = { "linkml_meta": {'alias': 'owner',
         'any_of': [{'range': 'User'}, {'range': 'Organization'}, {'range': 'string'}],
         'domain_of': ['Governed'],
         'narrow_mappings': ['prov:wasAttributedTo', 'prov:wasAssociatedBy']} })
    wasDerivedFrom: Optional[str] = Field(default=None, description="""Reference to another item that this item implements or extends, e.g. a template Item definition.""", json_schema_extra = { "linkml_meta": {'alias': 'wasDerivedFrom',
         'any_of': [{'range': 'Item'},
                    {'range': 'ItemGroup'},
                    {'range': 'MetaDataVersion'},
                    {'range': 'CodeList'},
                    {'range': 'ReifiedConcept'},
                    {'range': 'ConceptProperty'},
                    {'range': 'Condition'},
                    {'range': 'Method'},
                    {'range': 'NominalOccurrence'},
                    {'range': 'Dataflow'},
                    {'range': 'CubeComponent'},
                    {'range': 'DataProduct'},
                    {'range': 'ProvisionAgreement'}],
         'domain_of': ['Governed'],
         'exact_mappings': ['prov:wasDerivedFrom']} })


class SourceItem(ConfiguredBaseModel):
    """
    A data source that provides the origin of information for an item
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://cdisc.org/define-json'})

    item: Optional[str] = Field(default=None, description="""Reference to an item""", json_schema_extra = { "linkml_meta": {'alias': 'item',
         'domain_of': ['RangeCheck',
                       'SourceItem',
                       'CubeComponent',
                       'ObservationRelationship']} })
    document: Optional[list[DocumentReference]] = Field(default=None, description="""Reference to an external document""", json_schema_extra = { "linkml_meta": {'alias': 'document', 'domain_of': ['SourceItem']} })
    resource: Optional[list[str]] = Field(default=None, description="""Path to a resource (e.g. File, FHIR datasource) that is the source of this item""", json_schema_extra = { "linkml_meta": {'alias': 'resource',
         'any_of': [{'range': 'Resource'}, {'range': 'string'}],
         'domain_of': ['SourceItem']} })
    coding: Optional[list[Coding]] = Field(default=None, description="""A coding that describes the source of the item""", json_schema_extra = { "linkml_meta": {'alias': 'coding', 'domain_of': ['Labelled', 'CodeListItem', 'SourceItem']} })


class Parameter(IdentifiableElement):
    """
    A variable element that describes an input used in a formal expression
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://cdisc.org/define-json'})

    dataType: Optional[DataType] = Field(default=None, description="""The data type of the parameter.""", json_schema_extra = { "linkml_meta": {'alias': 'dataType',
         'domain_of': ['Item', 'CodeList', 'Parameter', 'ReturnValue']} })
    codeList: Optional[list[str]] = Field(default=None, description="""A list of allowed values for the parameter.""", json_schema_extra = { "linkml_meta": {'alias': 'codeList', 'domain_of': ['Item', 'ConceptProperty', 'Parameter']} })
    value: Optional[str] = Field(default=None, description="""A specific bound value for the parameter.""", json_schema_extra = { "linkml_meta": {'alias': 'value', 'domain_of': ['Translation', 'Parameter', 'Timing']} })
    defaultValue: Optional[str] = Field(default=None, description="""A default value for the parameter.""", json_schema_extra = { "linkml_meta": {'alias': 'defaultValue', 'domain_of': ['Parameter']} })
    items: Optional[list[str]] = Field(default=None, description="""A list of item dependencies for the parameter.""", json_schema_extra = { "linkml_meta": {'alias': 'items',
         'any_of': [{'range': 'Item'},
                    {'range': 'Dimension'},
                    {'range': 'Measure'},
                    {'range': 'DataAttribute'}],
         'domain_of': ['MetaDataVersion', 'ItemGroup', 'Parameter']} })
    conceptProperty: Optional[list[str]] = Field(default=None, description="""Reference to a specific concept property that this parameter represents or modifies.""", json_schema_extra = { "linkml_meta": {'alias': 'conceptProperty', 'domain_of': ['Item', 'Parameter']} })
    applicableWhen: Optional[list[str]] = Field(default=None, description="""References to different situations that define when this parameter  is applicable or required in the containing expression. Multiple whereClauses are combined with OR logic: the parameter applies  if ANY referenced WhereClause matches.
Within each WhereClause, conditions are combined with AND logic. Example: applicableWhen: [\"WC.ADULT\", \"WC.PEDIATRIC\"] means the parameter  is needed when (all conditions in WC.ADULT are true) OR  (all conditions in WC.PEDIATRIC are true).""", json_schema_extra = { "linkml_meta": {'alias': 'applicableWhen',
         'domain_of': ['Item', 'ItemGroup', 'Parameter', 'Analysis']} })
    conditions: Optional[list[str]] = Field(default=None, description="""Validation conditions that constrain this parameter's value beyond controlled terminology. Multiple conditions are combined with AND logic: all must be satisfied. Use these for parameter validation rules, distinct from applicableWhen  which determines if the parameter is needed at all.
Example: A parameter AGE might have conditions ensuring it's >= 0 and <= 120. or conditions might make up part of a componsed expression.""", json_schema_extra = { "linkml_meta": {'alias': 'conditions',
         'domain_of': ['MetaDataVersion', 'WhereClause', 'Condition', 'Parameter']} })
    required: Optional[bool] = Field(default=False, description="""Indicates whether this parameter must be provided when the  containing expression is evaluated (technical constraint).""", json_schema_extra = { "linkml_meta": {'alias': 'required', 'domain_of': ['Parameter'], 'ifabsent': 'False'} })
    OID: str = Field(default=..., description="""Local identifier within this study/context. Use CDISC OID format for regulatory submissions, or simple strings for internal use.""", json_schema_extra = { "linkml_meta": {'alias': 'OID', 'domain_of': ['Identifiable']} })
    uuid: Optional[str] = Field(default=None, description="""Universal unique identifier""", json_schema_extra = { "linkml_meta": {'alias': 'uuid', 'domain_of': ['Identifiable']} })
    name: Optional[str] = Field(default=None, description="""Short name or identifier, used for field names""", json_schema_extra = { "linkml_meta": {'alias': 'name', 'domain_of': ['Labelled', 'Standard']} })
    description: Optional[Union[TranslatedText, str]] = Field(default=None, description="""Detailed description, shown in tooltips""", json_schema_extra = { "linkml_meta": {'alias': 'description',
         'any_of': [{'range': 'string'}, {'range': 'TranslatedText'}],
         'domain_of': ['Labelled', 'CodeListItem']} })
    coding: Optional[list[Coding]] = Field(default=None, description="""Semantic tags for this element""", json_schema_extra = { "linkml_meta": {'alias': 'coding', 'domain_of': ['Labelled', 'CodeListItem', 'SourceItem']} })
    label: Optional[Union[TranslatedText, str]] = Field(default=None, description="""Human-readable label, shown in UIs""", json_schema_extra = { "linkml_meta": {'alias': 'label',
         'any_of': [{'range': 'string'}, {'range': 'TranslatedText'}],
         'domain_of': ['Labelled'],
         'exact_mappings': ['skos:prefLabel']} })
    aliases: Optional[list[Union[TranslatedText, str]]] = Field(default=None, description="""Alternative name or identifier""", json_schema_extra = { "linkml_meta": {'alias': 'aliases',
         'any_of': [{'range': 'string'}, {'range': 'TranslatedText'}],
         'domain_of': ['Labelled', 'CodeListItem'],
         'exact_mappings': ['skos:altLabel']} })


class ReturnValue(IdentifiableElement):
    """
    An output specification that defines the details of what a formal expression returns
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://cdisc.org/define-json'})

    dataType: Optional[DataType] = Field(default=None, description="""The data type of the return value.""", json_schema_extra = { "linkml_meta": {'alias': 'dataType',
         'domain_of': ['Item', 'CodeList', 'Parameter', 'ReturnValue']} })
    valueList: Optional[list[str]] = Field(default=None, description="""A list of possible return values.""", json_schema_extra = { "linkml_meta": {'alias': 'valueList', 'domain_of': ['ReturnValue']} })
    OID: str = Field(default=..., description="""Local identifier within this study/context. Use CDISC OID format for regulatory submissions, or simple strings for internal use.""", json_schema_extra = { "linkml_meta": {'alias': 'OID', 'domain_of': ['Identifiable']} })
    uuid: Optional[str] = Field(default=None, description="""Universal unique identifier""", json_schema_extra = { "linkml_meta": {'alias': 'uuid', 'domain_of': ['Identifiable']} })
    name: Optional[str] = Field(default=None, description="""Short name or identifier, used for field names""", json_schema_extra = { "linkml_meta": {'alias': 'name', 'domain_of': ['Labelled', 'Standard']} })
    description: Optional[Union[TranslatedText, str]] = Field(default=None, description="""Detailed description, shown in tooltips""", json_schema_extra = { "linkml_meta": {'alias': 'description',
         'any_of': [{'range': 'string'}, {'range': 'TranslatedText'}],
         'domain_of': ['Labelled', 'CodeListItem']} })
    coding: Optional[list[Coding]] = Field(default=None, description="""Semantic tags for this element""", json_schema_extra = { "linkml_meta": {'alias': 'coding', 'domain_of': ['Labelled', 'CodeListItem', 'SourceItem']} })
    label: Optional[Union[TranslatedText, str]] = Field(default=None, description="""Human-readable label, shown in UIs""", json_schema_extra = { "linkml_meta": {'alias': 'label',
         'any_of': [{'range': 'string'}, {'range': 'TranslatedText'}],
         'domain_of': ['Labelled'],
         'exact_mappings': ['skos:prefLabel']} })
    aliases: Optional[list[Union[TranslatedText, str]]] = Field(default=None, description="""Alternative name or identifier""", json_schema_extra = { "linkml_meta": {'alias': 'aliases',
         'any_of': [{'range': 'string'}, {'range': 'TranslatedText'}],
         'domain_of': ['Labelled', 'CodeListItem'],
         'exact_mappings': ['skos:altLabel']} })


class Origin(ConfiguredBaseModel):
    """
    A provenance element that describes the source of data for an item
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://cdisc.org/define-json'})

    type: Optional[OriginType] = Field(default=None, description="""The type of origin: Assigned, Collected, Derived, Protocol, Predecessor, Not Available, or Other.""", json_schema_extra = { "linkml_meta": {'alias': 'type',
         'domain_of': ['ItemGroup',
                       'Method',
                       'Origin',
                       'Organization',
                       'Standard',
                       'Timing']} })
    source: Optional[OriginSource] = Field(default=None, description="""The source of the data, such as Investigator, Sponsor, Subject, or Vendor.""", json_schema_extra = { "linkml_meta": {'alias': 'source',
         'domain_of': ['Origin',
                       'SiteOrSponsorComment',
                       'DataProvider',
                       'ProvisionAgreement']} })
    sourceItems: Optional[list[SourceItem]] = Field(default=None, description="""Source items for this origin""", json_schema_extra = { "linkml_meta": {'alias': 'sourceItems', 'domain_of': ['Origin']} })
    documents: Optional[list[DocumentReference]] = Field(default=None, description="""Reference to a document that describes this origin in detail.""", json_schema_extra = { "linkml_meta": {'alias': 'documents', 'domain_of': ['Comment', 'Method', 'Origin']} })


class SiteOrSponsorComment(GovernedElement):
    """
    A feedback element that contains comments from a site or sponsor, distinct from the general Comment class
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://cdisc.org/define-json'})

    text: Union[TranslatedText, str] = Field(default=..., description="""The comment text.""", json_schema_extra = { "linkml_meta": {'alias': 'text',
         'any_of': [{'range': 'string'}, {'range': 'TranslatedText'}],
         'domain_of': ['Comment', 'SiteOrSponsorComment']} })
    sourceType: Optional[OriginSource] = Field(default=None, description="""who made the comment, such as Investigator, Sponsor.""", json_schema_extra = { "linkml_meta": {'alias': 'sourceType', 'domain_of': ['SiteOrSponsorComment']} })
    source: Optional[str] = Field(default=None, description="""ID of the comment provider""", json_schema_extra = { "linkml_meta": {'alias': 'source',
         'any_of': [{'range': 'User'}, {'range': 'Organization'}, {'range': 'string'}],
         'domain_of': ['Origin',
                       'SiteOrSponsorComment',
                       'DataProvider',
                       'ProvisionAgreement']} })
    OID: str = Field(default=..., description="""Local identifier within this study/context. Use CDISC OID format for regulatory submissions, or simple strings for internal use.""", json_schema_extra = { "linkml_meta": {'alias': 'OID', 'domain_of': ['Identifiable']} })
    uuid: Optional[str] = Field(default=None, description="""Universal unique identifier""", json_schema_extra = { "linkml_meta": {'alias': 'uuid', 'domain_of': ['Identifiable']} })
    name: Optional[str] = Field(default=None, description="""Short name or identifier, used for field names""", json_schema_extra = { "linkml_meta": {'alias': 'name', 'domain_of': ['Labelled', 'Standard']} })
    description: Optional[Union[TranslatedText, str]] = Field(default=None, description="""Detailed description, shown in tooltips""", json_schema_extra = { "linkml_meta": {'alias': 'description',
         'any_of': [{'range': 'string'}, {'range': 'TranslatedText'}],
         'domain_of': ['Labelled', 'CodeListItem']} })
    coding: Optional[list[Coding]] = Field(default=None, description="""Semantic tags for this element""", json_schema_extra = { "linkml_meta": {'alias': 'coding', 'domain_of': ['Labelled', 'CodeListItem', 'SourceItem']} })
    label: Optional[Union[TranslatedText, str]] = Field(default=None, description="""Human-readable label, shown in UIs""", json_schema_extra = { "linkml_meta": {'alias': 'label',
         'any_of': [{'range': 'string'}, {'range': 'TranslatedText'}],
         'domain_of': ['Labelled'],
         'exact_mappings': ['skos:prefLabel']} })
    aliases: Optional[list[Union[TranslatedText, str]]] = Field(default=None, description="""Alternative name or identifier""", json_schema_extra = { "linkml_meta": {'alias': 'aliases',
         'any_of': [{'range': 'string'}, {'range': 'TranslatedText'}],
         'domain_of': ['Labelled', 'CodeListItem'],
         'exact_mappings': ['skos:altLabel']} })
    mandatory: Optional[bool] = Field(default=None, description="""Is this element required?""", json_schema_extra = { "linkml_meta": {'alias': 'mandatory', 'domain_of': ['Governed']} })
    comments: Optional[list[str]] = Field(default=None, description="""Comment on the element, such as a rationale for its inclusion or exclusion""", json_schema_extra = { "linkml_meta": {'alias': 'comments', 'domain_of': ['Governed']} })
    siteOrSponsorComments: Optional[list[str]] = Field(default=None, description="""Comment on the element, such as a rationale for its inclusion or exclusion""", json_schema_extra = { "linkml_meta": {'alias': 'siteOrSponsorComments', 'domain_of': ['Governed']} })
    purpose: Optional[Union[TranslatedText, str]] = Field(default=None, description="""Purpose or rationale for this data element""", json_schema_extra = { "linkml_meta": {'alias': 'purpose',
         'any_of': [{'range': 'string'}, {'range': 'TranslatedText'}],
         'domain_of': ['Governed']} })
    lastUpdated: Optional[datetime ] = Field(default=None, description="""When the resource was last updated""", json_schema_extra = { "linkml_meta": {'alias': 'lastUpdated', 'domain_of': ['Governed']} })
    owner: Optional[str] = Field(default=None, description="""Party responsible for this element""", json_schema_extra = { "linkml_meta": {'alias': 'owner',
         'any_of': [{'range': 'User'}, {'range': 'Organization'}, {'range': 'string'}],
         'domain_of': ['Governed'],
         'narrow_mappings': ['prov:wasAttributedTo', 'prov:wasAssociatedBy']} })
    wasDerivedFrom: Optional[str] = Field(default=None, description="""Reference to another item that this item implements or extends, e.g. a template Item definition.""", json_schema_extra = { "linkml_meta": {'alias': 'wasDerivedFrom',
         'any_of': [{'range': 'Item'},
                    {'range': 'ItemGroup'},
                    {'range': 'MetaDataVersion'},
                    {'range': 'CodeList'},
                    {'range': 'ReifiedConcept'},
                    {'range': 'ConceptProperty'},
                    {'range': 'Condition'},
                    {'range': 'Method'},
                    {'range': 'NominalOccurrence'},
                    {'range': 'Dataflow'},
                    {'range': 'CubeComponent'},
                    {'range': 'DataProduct'},
                    {'range': 'ProvisionAgreement'}],
         'domain_of': ['Governed'],
         'exact_mappings': ['prov:wasDerivedFrom']} })


class User(IdentifiableElement):
    """
    An entity that represents information about a specific user of a clinical data collection or data management system
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'broad_mappings': ['prov:Agent'],
         'exact_mappings': ['odm:User'],
         'from_schema': 'https://cdisc.org/define-json'})

    userType: Optional[UserType] = Field(default=None, description="""User's role in the study.""", json_schema_extra = { "linkml_meta": {'alias': 'userType', 'domain_of': ['User']} })
    userName: Optional[str] = Field(default=None, description="""The username of the user.""", json_schema_extra = { "linkml_meta": {'alias': 'userName', 'domain_of': ['User']} })
    fullName: Optional[str] = Field(default=None, description="""The full name of the user.""", json_schema_extra = { "linkml_meta": {'alias': 'fullName', 'domain_of': ['User']} })
    organization: Optional[str] = Field(default=None, description="""The organization the user belongs to.""", json_schema_extra = { "linkml_meta": {'alias': 'organization',
         'close_mappings': ['prov:actedOnBehalfOf'],
         'domain_of': ['User']} })
    OID: str = Field(default=..., description="""Local identifier within this study/context. Use CDISC OID format for regulatory submissions, or simple strings for internal use.""", json_schema_extra = { "linkml_meta": {'alias': 'OID', 'domain_of': ['Identifiable']} })
    uuid: Optional[str] = Field(default=None, description="""Universal unique identifier""", json_schema_extra = { "linkml_meta": {'alias': 'uuid', 'domain_of': ['Identifiable']} })
    name: Optional[str] = Field(default=None, description="""Short name or identifier, used for field names""", json_schema_extra = { "linkml_meta": {'alias': 'name', 'domain_of': ['Labelled', 'Standard']} })
    description: Optional[Union[TranslatedText, str]] = Field(default=None, description="""Detailed description, shown in tooltips""", json_schema_extra = { "linkml_meta": {'alias': 'description',
         'any_of': [{'range': 'string'}, {'range': 'TranslatedText'}],
         'domain_of': ['Labelled', 'CodeListItem']} })
    coding: Optional[list[Coding]] = Field(default=None, description="""Semantic tags for this element""", json_schema_extra = { "linkml_meta": {'alias': 'coding', 'domain_of': ['Labelled', 'CodeListItem', 'SourceItem']} })
    label: Optional[Union[TranslatedText, str]] = Field(default=None, description="""Human-readable label, shown in UIs""", json_schema_extra = { "linkml_meta": {'alias': 'label',
         'any_of': [{'range': 'string'}, {'range': 'TranslatedText'}],
         'domain_of': ['Labelled'],
         'exact_mappings': ['skos:prefLabel']} })
    aliases: Optional[list[Union[TranslatedText, str]]] = Field(default=None, description="""Alternative name or identifier""", json_schema_extra = { "linkml_meta": {'alias': 'aliases',
         'any_of': [{'range': 'string'}, {'range': 'TranslatedText'}],
         'domain_of': ['Labelled', 'CodeListItem'],
         'exact_mappings': ['skos:altLabel']} })


class Organization(IdentifiableElement):
    """
    An entity that represents organizational information, such as a site or sponsor
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'broad_mappings': ['prov:Agent'],
         'exact_mappings': ['odm:Organization',
                            'usdm:Organization',
                            'sdmx:Organisation'],
         'from_schema': 'https://cdisc.org/define-json'})

    role: Optional[str] = Field(default=None, description="""The role of the organization in the study.""", json_schema_extra = { "linkml_meta": {'alias': 'role', 'domain_of': ['IsODMItem', 'Organization', 'CubeComponent']} })
    type: Optional[OrganizationType] = Field(default=None, description="""The type of organization (e.g., site, sponsor, vendor).""", json_schema_extra = { "linkml_meta": {'alias': 'type',
         'domain_of': ['ItemGroup',
                       'Method',
                       'Origin',
                       'Organization',
                       'Standard',
                       'Timing']} })
    location: Optional[str] = Field(default=None, description="""The physical location of the organization.""", json_schema_extra = { "linkml_meta": {'alias': 'location', 'domain_of': ['Organization', 'Display']} })
    address: Optional[str] = Field(default=None, description="""The address of the organization.""", json_schema_extra = { "linkml_meta": {'alias': 'address', 'domain_of': ['Organization']} })
    partOfOrganization: Optional[str] = Field(default=None, description="""Reference to a parent organization if this organization is part of a larger entity.""", json_schema_extra = { "linkml_meta": {'alias': 'partOfOrganization', 'domain_of': ['Organization']} })
    OID: str = Field(default=..., description="""Local identifier within this study/context. Use CDISC OID format for regulatory submissions, or simple strings for internal use.""", json_schema_extra = { "linkml_meta": {'alias': 'OID', 'domain_of': ['Identifiable']} })
    uuid: Optional[str] = Field(default=None, description="""Universal unique identifier""", json_schema_extra = { "linkml_meta": {'alias': 'uuid', 'domain_of': ['Identifiable']} })
    name: Optional[str] = Field(default=None, description="""Short name or identifier, used for field names""", json_schema_extra = { "linkml_meta": {'alias': 'name', 'domain_of': ['Labelled', 'Standard']} })
    description: Optional[Union[TranslatedText, str]] = Field(default=None, description="""Detailed description, shown in tooltips""", json_schema_extra = { "linkml_meta": {'alias': 'description',
         'any_of': [{'range': 'string'}, {'range': 'TranslatedText'}],
         'domain_of': ['Labelled', 'CodeListItem']} })
    coding: Optional[list[Coding]] = Field(default=None, description="""Semantic tags for this element""", json_schema_extra = { "linkml_meta": {'alias': 'coding', 'domain_of': ['Labelled', 'CodeListItem', 'SourceItem']} })
    label: Optional[Union[TranslatedText, str]] = Field(default=None, description="""Human-readable label, shown in UIs""", json_schema_extra = { "linkml_meta": {'alias': 'label',
         'any_of': [{'range': 'string'}, {'range': 'TranslatedText'}],
         'domain_of': ['Labelled'],
         'exact_mappings': ['skos:prefLabel']} })
    aliases: Optional[list[Union[TranslatedText, str]]] = Field(default=None, description="""Alternative name or identifier""", json_schema_extra = { "linkml_meta": {'alias': 'aliases',
         'any_of': [{'range': 'string'}, {'range': 'TranslatedText'}],
         'domain_of': ['Labelled', 'CodeListItem'],
         'exact_mappings': ['skos:altLabel']} })


class Standard(IdentifiableElement):
    """
    A collection element that groups related standards within a specific context, used for defining CDISC implementation guides and controlled terminologies
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://cdisc.org/define-json'})

    name: Optional[StandardName] = Field(default=None, description="""Name of a standard""", json_schema_extra = { "linkml_meta": {'alias': 'name', 'domain_of': ['Labelled', 'Standard']} })
    type: Optional[StandardType] = Field(default=None, description="""Type of a standard""", json_schema_extra = { "linkml_meta": {'alias': 'type',
         'domain_of': ['ItemGroup',
                       'Method',
                       'Origin',
                       'Organization',
                       'Standard',
                       'Timing']} })
    publishingSet: Optional[PublishingSet] = Field(default=None, description="""Publishing Set of a Controlled Terminology""", json_schema_extra = { "linkml_meta": {'alias': 'publishingSet', 'domain_of': ['Standard']} })
    version: Optional[str] = Field(default=None, description="""Version of an Implementation Guide or of a Controlled Terminology""", json_schema_extra = { "linkml_meta": {'alias': 'version', 'domain_of': ['Versioned', 'Standard']} })
    status: Optional[StandardStatus] = Field(default=None, description="""Status of an Implementation Guide or of a Controlled Terminology""", json_schema_extra = { "linkml_meta": {'alias': 'status', 'domain_of': ['Standard']} })
    OID: str = Field(default=..., description="""Local identifier within this study/context. Use CDISC OID format for regulatory submissions, or simple strings for internal use.""", json_schema_extra = { "linkml_meta": {'alias': 'OID', 'domain_of': ['Identifiable']} })
    uuid: Optional[str] = Field(default=None, description="""Universal unique identifier""", json_schema_extra = { "linkml_meta": {'alias': 'uuid', 'domain_of': ['Identifiable']} })
    description: Optional[Union[TranslatedText, str]] = Field(default=None, description="""Detailed description, shown in tooltips""", json_schema_extra = { "linkml_meta": {'alias': 'description',
         'any_of': [{'range': 'string'}, {'range': 'TranslatedText'}],
         'domain_of': ['Labelled', 'CodeListItem']} })
    coding: Optional[list[Coding]] = Field(default=None, description="""Semantic tags for this element""", json_schema_extra = { "linkml_meta": {'alias': 'coding', 'domain_of': ['Labelled', 'CodeListItem', 'SourceItem']} })
    label: Optional[Union[TranslatedText, str]] = Field(default=None, description="""Human-readable label, shown in UIs""", json_schema_extra = { "linkml_meta": {'alias': 'label',
         'any_of': [{'range': 'string'}, {'range': 'TranslatedText'}],
         'domain_of': ['Labelled'],
         'exact_mappings': ['skos:prefLabel']} })
    aliases: Optional[list[Union[TranslatedText, str]]] = Field(default=None, description="""Alternative name or identifier""", json_schema_extra = { "linkml_meta": {'alias': 'aliases',
         'any_of': [{'range': 'string'}, {'range': 'TranslatedText'}],
         'domain_of': ['Labelled', 'CodeListItem'],
         'exact_mappings': ['skos:altLabel']} })


class Resource(Versioned, IdentifiableElement):
    """
    An external reference that serves as the source for a Dataset, ItemGroup, or Item
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'close_mappings': ['odm:Resource'],
         'from_schema': 'https://cdisc.org/define-json',
         'mixins': ['Versioned']})

    resourceType: Optional[str] = Field(default=None, description="""Type of resource (e.g.,  \"ODM\", \"HL7-FHIR\", \"HL7-CDA\", \"HL7-v2\", \"OpenEHR-extract\")""", json_schema_extra = { "linkml_meta": {'alias': 'resourceType', 'domain_of': ['Resource']} })
    attribute: Optional[str] = Field(default=None, description="""Field provided by the Name attribute where the data or information can be obtained. Examples are \"valueQuantity.value\" or \"valueQuantity.unit\".""", json_schema_extra = { "linkml_meta": {'alias': 'attribute',
         'domain_of': ['Resource',
                       'MeasureRelationship',
                       'DataflowRelationship',
                       'GroupRelationship',
                       'DimensionRelationship',
                       'ObservationRelationship']} })
    selection: Optional[list[FormalExpression]] = Field(default=None, description="""Machine-executable instructions for selecting data from the resource.""", json_schema_extra = { "linkml_meta": {'alias': 'selection', 'domain_of': ['Resource']} })
    version: Optional[str] = Field(default=None, description="""The version of the external resources""", json_schema_extra = { "linkml_meta": {'alias': 'version', 'domain_of': ['Versioned', 'Standard']} })
    href: Optional[str] = Field(default=None, description="""Machine-readable instructions to obtain the resource e.g. FHIR path, URL""", json_schema_extra = { "linkml_meta": {'alias': 'href', 'domain_of': ['Versioned']} })
    OID: str = Field(default=..., description="""Local identifier within this study/context. Use CDISC OID format for regulatory submissions, or simple strings for internal use.""", json_schema_extra = { "linkml_meta": {'alias': 'OID', 'domain_of': ['Identifiable']} })
    uuid: Optional[str] = Field(default=None, description="""Universal unique identifier""", json_schema_extra = { "linkml_meta": {'alias': 'uuid', 'domain_of': ['Identifiable']} })
    name: Optional[str] = Field(default=None, description="""Short name or identifier, used for field names""", json_schema_extra = { "linkml_meta": {'alias': 'name', 'domain_of': ['Labelled', 'Standard']} })
    description: Optional[Union[TranslatedText, str]] = Field(default=None, description="""Detailed description, shown in tooltips""", json_schema_extra = { "linkml_meta": {'alias': 'description',
         'any_of': [{'range': 'string'}, {'range': 'TranslatedText'}],
         'domain_of': ['Labelled', 'CodeListItem']} })
    coding: Optional[list[Coding]] = Field(default=None, description="""Semantic tags for this element""", json_schema_extra = { "linkml_meta": {'alias': 'coding', 'domain_of': ['Labelled', 'CodeListItem', 'SourceItem']} })
    label: Optional[Union[TranslatedText, str]] = Field(default=None, description="""Human-readable label, shown in UIs""", json_schema_extra = { "linkml_meta": {'alias': 'label',
         'any_of': [{'range': 'string'}, {'range': 'TranslatedText'}],
         'domain_of': ['Labelled'],
         'exact_mappings': ['skos:prefLabel']} })
    aliases: Optional[list[Union[TranslatedText, str]]] = Field(default=None, description="""Alternative name or identifier""", json_schema_extra = { "linkml_meta": {'alias': 'aliases',
         'any_of': [{'range': 'string'}, {'range': 'TranslatedText'}],
         'domain_of': ['Labelled', 'CodeListItem'],
         'exact_mappings': ['skos:altLabel']} })


class DocumentReference(Versioned, IdentifiableElement):
    """
    A comprehensive reference element that points to an external document, combining elements from ODM and FHIR
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://cdisc.org/define-json', 'mixins': ['Versioned']})

    title: Optional[str] = Field(default=None, description="""Document title""", json_schema_extra = { "linkml_meta": {'alias': 'title', 'domain_of': ['DocumentReference']} })
    leafID: Optional[str] = Field(default=None, description="""Leaf identifier for document reference in Define-XML""", json_schema_extra = { "linkml_meta": {'alias': 'leafID', 'domain_of': ['DocumentReference']} })
    pages: Optional[list[int]] = Field(default=None, description="""Reference to specific pages in a PDF document""", json_schema_extra = { "linkml_meta": {'alias': 'pages', 'domain_of': ['DocumentReference']} })
    relationship: Optional[str] = Field(default=None, description="""Relationship to the referencing entity""", json_schema_extra = { "linkml_meta": {'alias': 'relationship', 'domain_of': ['DocumentReference']} })
    version: Optional[str] = Field(default=None, description="""The version of the external resources""", json_schema_extra = { "linkml_meta": {'alias': 'version', 'domain_of': ['Versioned', 'Standard']} })
    href: Optional[str] = Field(default=None, description="""Machine-readable instructions to obtain the resource e.g. FHIR path, URL""", json_schema_extra = { "linkml_meta": {'alias': 'href', 'domain_of': ['Versioned']} })
    OID: str = Field(default=..., description="""Local identifier within this study/context. Use CDISC OID format for regulatory submissions, or simple strings for internal use.""", json_schema_extra = { "linkml_meta": {'alias': 'OID', 'domain_of': ['Identifiable']} })
    uuid: Optional[str] = Field(default=None, description="""Universal unique identifier""", json_schema_extra = { "linkml_meta": {'alias': 'uuid', 'domain_of': ['Identifiable']} })
    name: Optional[str] = Field(default=None, description="""Short name or identifier, used for field names""", json_schema_extra = { "linkml_meta": {'alias': 'name', 'domain_of': ['Labelled', 'Standard']} })
    description: Optional[Union[TranslatedText, str]] = Field(default=None, description="""Detailed description, shown in tooltips""", json_schema_extra = { "linkml_meta": {'alias': 'description',
         'any_of': [{'range': 'string'}, {'range': 'TranslatedText'}],
         'domain_of': ['Labelled', 'CodeListItem']} })
    coding: Optional[list[Coding]] = Field(default=None, description="""Semantic tags for this element""", json_schema_extra = { "linkml_meta": {'alias': 'coding', 'domain_of': ['Labelled', 'CodeListItem', 'SourceItem']} })
    label: Optional[Union[TranslatedText, str]] = Field(default=None, description="""Human-readable label, shown in UIs""", json_schema_extra = { "linkml_meta": {'alias': 'label',
         'any_of': [{'range': 'string'}, {'range': 'TranslatedText'}],
         'domain_of': ['Labelled'],
         'exact_mappings': ['skos:prefLabel']} })
    aliases: Optional[list[Union[TranslatedText, str]]] = Field(default=None, description="""Alternative name or identifier""", json_schema_extra = { "linkml_meta": {'alias': 'aliases',
         'any_of': [{'range': 'string'}, {'range': 'TranslatedText'}],
         'domain_of': ['Labelled', 'CodeListItem'],
         'exact_mappings': ['skos:altLabel']} })


class Timing(IdentifiableElement):
    """
    A temporal element that describes the timing of an event or occurrence, which can be absolute, relative, or nominal
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'broad_mappings': ['fhir:Timing'],
         'exact_mappings': ['usdm:Timing'],
         'from_schema': 'https://cdisc.org/define-json',
         'narrow_mappings': ['omop:Observation_period',
                             'omop:Drug_era',
                             'omop:Condition_era',
                             'omop:Procedure_era',
                             'fhir:Period',
                             'fhir:Age',
                             'fhir:Duration']})

    type: TimingType = Field(default=..., description="""The type of timing: Fixed, Before (Relative), or After (Relative).""", json_schema_extra = { "linkml_meta": {'alias': 'type',
         'domain_of': ['ItemGroup',
                       'Method',
                       'Origin',
                       'Organization',
                       'Standard',
                       'Timing']} })
    isNominal: Optional[bool] = Field(default=None, description="""Indicates whether the timing is nominal (event-based) or not.""", json_schema_extra = { "linkml_meta": {'alias': 'isNominal', 'domain_of': ['Timing']} })
    value: str = Field(default=..., description="""The value of the timing, which can be a date/time, duration, or event reference.""", json_schema_extra = { "linkml_meta": {'alias': 'value', 'domain_of': ['Translation', 'Parameter', 'Timing']} })
    relativeTo: Optional[str] = Field(default=None, description="""Reference to the event or occurrence that this timing is relative to.""", json_schema_extra = { "linkml_meta": {'alias': 'relativeTo', 'domain_of': ['Timing']} })
    relativeFrom: Optional[str] = Field(default=None, description="""Reference to the event or occurrence that this timing is relative to.""", json_schema_extra = { "linkml_meta": {'alias': 'relativeFrom', 'domain_of': ['Timing']} })
    windowLower: Optional[datetime ] = Field(default=None, description="""Start date/time of the timing""", json_schema_extra = { "linkml_meta": {'alias': 'windowLower', 'domain_of': ['Timing']} })
    windowUpper: Optional[datetime ] = Field(default=None, description="""End date/time of the timing""", json_schema_extra = { "linkml_meta": {'alias': 'windowUpper', 'domain_of': ['Timing']} })
    recalled: Optional[bool] = Field(default=None, description="""Indicates whether the timing is recalled or not (recalled timings are less reliable).""", json_schema_extra = { "linkml_meta": {'alias': 'recalled', 'domain_of': ['Timing']} })
    frequency: Optional[str] = Field(default=None, description="""Frequency. Use dose frequency terminology e.g. \"BID\" if applicable.""", json_schema_extra = { "linkml_meta": {'alias': 'frequency', 'domain_of': ['Timing']} })
    imputation: Optional[str] = Field(default=None, description="""The imputation method used for the Timing.""", json_schema_extra = { "linkml_meta": {'alias': 'imputation', 'domain_of': ['Timing', 'CubeComponent']} })
    OID: str = Field(default=..., description="""Local identifier within this study/context. Use CDISC OID format for regulatory submissions, or simple strings for internal use.""", json_schema_extra = { "linkml_meta": {'alias': 'OID', 'domain_of': ['Identifiable']} })
    uuid: Optional[str] = Field(default=None, description="""Universal unique identifier""", json_schema_extra = { "linkml_meta": {'alias': 'uuid', 'domain_of': ['Identifiable']} })
    name: Optional[str] = Field(default=None, description="""Short name or identifier, used for field names""", json_schema_extra = { "linkml_meta": {'alias': 'name', 'domain_of': ['Labelled', 'Standard']} })
    description: Optional[Union[TranslatedText, str]] = Field(default=None, description="""Detailed description, shown in tooltips""", json_schema_extra = { "linkml_meta": {'alias': 'description',
         'any_of': [{'range': 'string'}, {'range': 'TranslatedText'}],
         'domain_of': ['Labelled', 'CodeListItem']} })
    coding: Optional[list[Coding]] = Field(default=None, description="""Semantic tags for this element""", json_schema_extra = { "linkml_meta": {'alias': 'coding', 'domain_of': ['Labelled', 'CodeListItem', 'SourceItem']} })
    label: Optional[Union[TranslatedText, str]] = Field(default=None, description="""Human-readable label, shown in UIs""", json_schema_extra = { "linkml_meta": {'alias': 'label',
         'any_of': [{'range': 'string'}, {'range': 'TranslatedText'}],
         'domain_of': ['Labelled'],
         'exact_mappings': ['skos:prefLabel']} })
    aliases: Optional[list[Union[TranslatedText, str]]] = Field(default=None, description="""Alternative name or identifier""", json_schema_extra = { "linkml_meta": {'alias': 'aliases',
         'any_of': [{'range': 'string'}, {'range': 'TranslatedText'}],
         'domain_of': ['Labelled', 'CodeListItem'],
         'exact_mappings': ['skos:altLabel']} })


class NominalOccurrence(GovernedElement):
    """
    An event element that represents occurrences such as planned or unplanned encounters or adverse events
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://cdisc.org/define-json',
         'narrow_mappings': ['usdm:ScheduledInstance',
                             'usdm:Encounter',
                             'usdm:InterCurrentEvent',
                             'fhir:PlanDefinition/action',
                             'fhir:ActivityDefinition',
                             'fhir:Encounter',
                             'fhir:AdverseEvent',
                             'omop:Visit_occurrence',
                             'omop:Condition_occurrence',
                             'omop:Procedure_occurrence']})

    timing: str = Field(default=..., description="""A named event reference, that can nest further named timing references.""", json_schema_extra = { "linkml_meta": {'alias': 'timing', 'domain_of': ['NominalOccurrence']} })
    event: Optional[str] = Field(default=None, description="""The ID of the event in a Schedule.""", json_schema_extra = { "linkml_meta": {'alias': 'event', 'domain_of': ['NominalOccurrence']} })
    condition: Optional[list[str]] = Field(default=None, description="""A condition that must be met for this occurrence to be valid.""", json_schema_extra = { "linkml_meta": {'alias': 'condition', 'domain_of': ['NominalOccurrence']} })
    OID: str = Field(default=..., description="""Local identifier within this study/context. Use CDISC OID format for regulatory submissions, or simple strings for internal use.""", json_schema_extra = { "linkml_meta": {'alias': 'OID', 'domain_of': ['Identifiable']} })
    uuid: Optional[str] = Field(default=None, description="""Universal unique identifier""", json_schema_extra = { "linkml_meta": {'alias': 'uuid', 'domain_of': ['Identifiable']} })
    name: Optional[str] = Field(default=None, description="""Short name or identifier, used for field names""", json_schema_extra = { "linkml_meta": {'alias': 'name', 'domain_of': ['Labelled', 'Standard']} })
    description: Optional[Union[TranslatedText, str]] = Field(default=None, description="""Detailed description, shown in tooltips""", json_schema_extra = { "linkml_meta": {'alias': 'description',
         'any_of': [{'range': 'string'}, {'range': 'TranslatedText'}],
         'domain_of': ['Labelled', 'CodeListItem']} })
    coding: Optional[list[Coding]] = Field(default=None, description="""Semantic tags for this element""", json_schema_extra = { "linkml_meta": {'alias': 'coding', 'domain_of': ['Labelled', 'CodeListItem', 'SourceItem']} })
    label: Optional[Union[TranslatedText, str]] = Field(default=None, description="""Human-readable label, shown in UIs""", json_schema_extra = { "linkml_meta": {'alias': 'label',
         'any_of': [{'range': 'string'}, {'range': 'TranslatedText'}],
         'domain_of': ['Labelled'],
         'exact_mappings': ['skos:prefLabel']} })
    aliases: Optional[list[Union[TranslatedText, str]]] = Field(default=None, description="""Alternative name or identifier""", json_schema_extra = { "linkml_meta": {'alias': 'aliases',
         'any_of': [{'range': 'string'}, {'range': 'TranslatedText'}],
         'domain_of': ['Labelled', 'CodeListItem'],
         'exact_mappings': ['skos:altLabel']} })
    mandatory: Optional[bool] = Field(default=None, description="""Is this element required?""", json_schema_extra = { "linkml_meta": {'alias': 'mandatory', 'domain_of': ['Governed']} })
    comments: Optional[list[str]] = Field(default=None, description="""Comment on the element, such as a rationale for its inclusion or exclusion""", json_schema_extra = { "linkml_meta": {'alias': 'comments', 'domain_of': ['Governed']} })
    siteOrSponsorComments: Optional[list[str]] = Field(default=None, description="""Comment on the element, such as a rationale for its inclusion or exclusion""", json_schema_extra = { "linkml_meta": {'alias': 'siteOrSponsorComments', 'domain_of': ['Governed']} })
    purpose: Optional[Union[TranslatedText, str]] = Field(default=None, description="""Purpose or rationale for this data element""", json_schema_extra = { "linkml_meta": {'alias': 'purpose',
         'any_of': [{'range': 'string'}, {'range': 'TranslatedText'}],
         'domain_of': ['Governed']} })
    lastUpdated: Optional[datetime ] = Field(default=None, description="""When the resource was last updated""", json_schema_extra = { "linkml_meta": {'alias': 'lastUpdated', 'domain_of': ['Governed']} })
    owner: Optional[str] = Field(default=None, description="""Party responsible for this element""", json_schema_extra = { "linkml_meta": {'alias': 'owner',
         'any_of': [{'range': 'User'}, {'range': 'Organization'}, {'range': 'string'}],
         'domain_of': ['Governed'],
         'narrow_mappings': ['prov:wasAttributedTo', 'prov:wasAssociatedBy']} })
    wasDerivedFrom: Optional[str] = Field(default=None, description="""Reference to another item that this item implements or extends, e.g. a template Item definition.""", json_schema_extra = { "linkml_meta": {'alias': 'wasDerivedFrom',
         'any_of': [{'range': 'Item'},
                    {'range': 'ItemGroup'},
                    {'range': 'MetaDataVersion'},
                    {'range': 'CodeList'},
                    {'range': 'ReifiedConcept'},
                    {'range': 'ConceptProperty'},
                    {'range': 'Condition'},
                    {'range': 'Method'},
                    {'range': 'NominalOccurrence'},
                    {'range': 'Dataflow'},
                    {'range': 'CubeComponent'},
                    {'range': 'DataProduct'},
                    {'range': 'ProvisionAgreement'}],
         'domain_of': ['Governed'],
         'exact_mappings': ['prov:wasDerivedFrom']} })


class DataStructureDefinition(ItemGroup):
    """
    A structural element that defines the organization of a data cube for analysis, including dimensions, attributes, and measures
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'close_mappings': ['sdmx:DataStructureDefinition',
                            'qb:DataStructureDefinition'],
         'from_schema': 'https://cdisc.org/define-json'})

    dimensions: Optional[list[str]] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'dimensions',
         'domain_of': ['DataStructureDefinition', 'DimensionRelationship']} })
    measures: Optional[list[str]] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'measures', 'domain_of': ['DataStructureDefinition']} })
    attributes: Optional[list[str]] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'attributes', 'domain_of': ['DataStructureDefinition']} })
    grouping: Optional[str] = Field(default=None, description="""An association to a set of metadata concepts that have an identified structural role in a Data Structure Definition.""", json_schema_extra = { "linkml_meta": {'alias': 'grouping', 'domain_of': ['DataStructureDefinition']} })
    evolvingStructure: Optional[bool] = Field(default=False, json_schema_extra = { "linkml_meta": {'alias': 'evolvingStructure',
         'domain_of': ['DataStructureDefinition'],
         'ifabsent': 'False'} })
    domain: Optional[str] = Field(default=None, description="""Domain abbreviation for the dataset.""", json_schema_extra = { "linkml_meta": {'alias': 'domain', 'domain_of': ['ItemGroup', 'DataProduct']} })
    structure: Optional[Union[TranslatedText, str]] = Field(default=None, description="""Data structure of the item group, indicating how the records are organized. If this is a FHIR Resource, is it nested or flattened? If this is a structured concept, is it a Biomedical/Derivation/Analysis concept?""", json_schema_extra = { "linkml_meta": {'alias': 'structure',
         'any_of': [{'range': 'string'}, {'range': 'TranslatedText'}],
         'domain_of': ['ItemGroup', 'Dataflow']} })
    isReferenceData: Optional[bool] = Field(default=None, description="""Set to Yes if this is a reference item group.""", json_schema_extra = { "linkml_meta": {'alias': 'isReferenceData', 'domain_of': ['ItemGroup']} })
    type: Optional[ItemGroupType] = Field(default=None, description="""Type of item group""", json_schema_extra = { "linkml_meta": {'alias': 'type',
         'domain_of': ['ItemGroup',
                       'Method',
                       'Origin',
                       'Organization',
                       'Standard',
                       'Timing']} })
    items: Optional[list[Item]] = Field(default=None, description="""Items in this group""", json_schema_extra = { "linkml_meta": {'alias': 'items',
         'close_mappings': ['fhir:StructureDefinition/snapshot',
                            'fhir:StructureDefinition/differential'],
         'domain_of': ['MetaDataVersion', 'ItemGroup', 'Parameter']} })
    keySequence: Optional[list[str]] = Field(default=None, description="""Ordered list of Items that define the dataset key structure for sorting and uniqueness. Each entry is an OID reference to an Item in the items array. Order determines sorting precedence, merge operations, and record uniqueness. These are allowed to be null, unlike stricter dataset dimensions or primary keys.""", json_schema_extra = { "linkml_meta": {'alias': 'keySequence',
        'close_mappings': ['odm:ItemRef.KeySequence', 'sdmx:DimensionDescriptor'],
        'domain_of': ['ItemGroup']} })
    slices: Optional[list[Union[ItemGroup, str]]] = Field(default=None, description="""Child ItemGroups nested within this item group (e.g., ValueLists under parent domains). Can be either: - Full ItemGroup objects (preferred for hierarchical nesting) - OID string references (for cross-references to avoid duplication)""", json_schema_extra = { "linkml_meta": {'alias': 'slices',
        'any_of': [{'range': 'ItemGroup'}, {'range': 'string'}],
        'domain_of': ['ItemGroup']} })
    implementsConcept: Optional[str] = Field(default=None, description="""Reference to a abstract concept topic that this item group is a specialization of""", json_schema_extra = { "linkml_meta": {'alias': 'implementsConcept', 'domain_of': ['ItemGroup', 'Method']} })
    applicableWhen: Optional[list[str]] = Field(default=None, description="""References to different situations that define when this item applies.
Multiple whereClauses are combined with OR logic: the item applies if ANY referenced WhereClause matches.
Within each WhereClause, conditions are combined with AND logic: all conditions must be true.

Example: whereClause: [\"WC.SYSBP\", \"WC.DIABP\"] means the item applies when
(all conditions in WC.SYSBP are true) OR (all conditions in WC.DIABP are true).
""", json_schema_extra = { "linkml_meta": {'alias': 'applicableWhen',
         'close_mappings': ['fhir:StructureDefinition/context'],
         'domain_of': ['Item', 'ItemGroup', 'Parameter', 'Analysis']} })
    profile: Optional[list[str]] = Field(default=None, description="""Profiles this resource claims to conform to""", json_schema_extra = { "linkml_meta": {'alias': 'profile', 'domain_of': ['IsProfile']} })
    security: Optional[list[Coding]] = Field(default=None, description="""Security tags applied to this resource""", json_schema_extra = { "linkml_meta": {'alias': 'security', 'domain_of': ['IsProfile']} })
    authenticator: Optional[str] = Field(default=None, description="""Who/what authenticated the resource""", json_schema_extra = { "linkml_meta": {'alias': 'authenticator',
         'any_of': [{'range': 'User'}, {'range': 'Organization'}, {'range': 'string'}],
         'domain_of': ['IsProfile']} })
    validityPeriod: Optional[str] = Field(default=None, description="""Time period during which the resouce is valid""", json_schema_extra = { "linkml_meta": {'alias': 'validityPeriod', 'domain_of': ['IsProfile']} })
    OID: str = Field(default=..., description="""Local identifier within this study/context. Use CDISC OID format for regulatory submissions, or simple strings for internal use.""", json_schema_extra = { "linkml_meta": {'alias': 'OID', 'domain_of': ['Identifiable']} })
    uuid: Optional[str] = Field(default=None, description="""Universal unique identifier""", json_schema_extra = { "linkml_meta": {'alias': 'uuid', 'domain_of': ['Identifiable']} })
    name: Optional[str] = Field(default=None, description="""Short name or identifier, used for field names""", json_schema_extra = { "linkml_meta": {'alias': 'name', 'domain_of': ['Labelled', 'Standard']} })
    description: Optional[Union[TranslatedText, str]] = Field(default=None, description="""Detailed description, shown in tooltips""", json_schema_extra = { "linkml_meta": {'alias': 'description',
         'any_of': [{'range': 'string'}, {'range': 'TranslatedText'}],
         'domain_of': ['Labelled', 'CodeListItem']} })
    coding: Optional[list[Coding]] = Field(default=None, description="""Semantic tags for this element""", json_schema_extra = { "linkml_meta": {'alias': 'coding', 'domain_of': ['Labelled', 'CodeListItem', 'SourceItem']} })
    label: Optional[Union[TranslatedText, str]] = Field(default=None, description="""Human-readable label, shown in UIs""", json_schema_extra = { "linkml_meta": {'alias': 'label',
         'any_of': [{'range': 'string'}, {'range': 'TranslatedText'}],
         'domain_of': ['Labelled'],
         'exact_mappings': ['skos:prefLabel']} })
    aliases: Optional[list[Union[TranslatedText, str]]] = Field(default=None, description="""Alternative name or identifier""", json_schema_extra = { "linkml_meta": {'alias': 'aliases',
         'any_of': [{'range': 'string'}, {'range': 'TranslatedText'}],
         'domain_of': ['Labelled', 'CodeListItem'],
         'exact_mappings': ['skos:altLabel']} })
    mandatory: Optional[bool] = Field(default=None, description="""Is this element required?""", json_schema_extra = { "linkml_meta": {'alias': 'mandatory', 'domain_of': ['Governed']} })
    comments: Optional[list[str]] = Field(default=None, description="""Comment on the element, such as a rationale for its inclusion or exclusion""", json_schema_extra = { "linkml_meta": {'alias': 'comments', 'domain_of': ['Governed']} })
    siteOrSponsorComments: Optional[list[str]] = Field(default=None, description="""Comment on the element, such as a rationale for its inclusion or exclusion""", json_schema_extra = { "linkml_meta": {'alias': 'siteOrSponsorComments', 'domain_of': ['Governed']} })
    purpose: Optional[Union[TranslatedText, str]] = Field(default=None, description="""Purpose or rationale for this data element""", json_schema_extra = { "linkml_meta": {'alias': 'purpose',
         'any_of': [{'range': 'string'}, {'range': 'TranslatedText'}],
         'domain_of': ['Governed']} })
    lastUpdated: Optional[datetime ] = Field(default=None, description="""When the resource was last updated""", json_schema_extra = { "linkml_meta": {'alias': 'lastUpdated', 'domain_of': ['Governed']} })
    owner: Optional[str] = Field(default=None, description="""Party responsible for this element""", json_schema_extra = { "linkml_meta": {'alias': 'owner',
         'any_of': [{'range': 'User'}, {'range': 'Organization'}, {'range': 'string'}],
         'domain_of': ['Governed'],
         'narrow_mappings': ['prov:wasAttributedTo', 'prov:wasAssociatedBy']} })
    wasDerivedFrom: Optional[str] = Field(default=None, description="""Reference to another item that this item implements or extends, e.g. a template Item definition.""", json_schema_extra = { "linkml_meta": {'alias': 'wasDerivedFrom',
         'any_of': [{'range': 'Item'},
                    {'range': 'ItemGroup'},
                    {'range': 'MetaDataVersion'},
                    {'range': 'CodeList'},
                    {'range': 'ReifiedConcept'},
                    {'range': 'ConceptProperty'},
                    {'range': 'Condition'},
                    {'range': 'Method'},
                    {'range': 'NominalOccurrence'},
                    {'range': 'Dataflow'},
                    {'range': 'CubeComponent'},
                    {'range': 'DataProduct'},
                    {'range': 'ProvisionAgreement'}],
         'domain_of': ['Governed'],
         'exact_mappings': ['prov:wasDerivedFrom']} })
    version: Optional[str] = Field(default=None, description="""The version of the external resources""", json_schema_extra = { "linkml_meta": {'alias': 'version', 'domain_of': ['Versioned', 'Standard']} })
    href: Optional[str] = Field(default=None, description="""Machine-readable instructions to obtain the resource e.g. FHIR path, URL""", json_schema_extra = { "linkml_meta": {'alias': 'href', 'domain_of': ['Versioned']} })


class Dataflow(Versioned, GovernedElement):
    """
    An abstract representation that defines data provision for different reference periods, where a Distribution and its Dataset are instances
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'close_mappings': ['sdmx:Dataflow'],
         'from_schema': 'https://cdisc.org/define-json',
         'mixins': ['Versioned'],
         'related_mappings': ['dprod:Distribution',
                              'dcat:Distribution',
                              'dprod:DataService',
                              'dcat:DataService']})

    structure: str = Field(default=..., description="""Structured component specification for this flow""", json_schema_extra = { "linkml_meta": {'alias': 'structure', 'domain_of': ['ItemGroup', 'Dataflow']} })
    dimensionConstraint: Optional[list[str]] = Field(default=None, description="""Subset of dimensions that are agreed upon by the dataflow and must be included.""", json_schema_extra = { "linkml_meta": {'alias': 'dimensionConstraint', 'domain_of': ['Dataflow']} })
    analysisMethod: Optional[str] = Field(default=None, description="""Metadata about the analysis method used to produce the data in this dataflow.""", json_schema_extra = { "linkml_meta": {'alias': 'analysisMethod', 'domain_of': ['Dataflow', 'Analysis']} })
    version: Optional[str] = Field(default=None, description="""The version of the external resources""", json_schema_extra = { "linkml_meta": {'alias': 'version', 'domain_of': ['Versioned', 'Standard']} })
    href: Optional[str] = Field(default=None, description="""Machine-readable instructions to obtain the resource e.g. FHIR path, URL""", json_schema_extra = { "linkml_meta": {'alias': 'href', 'domain_of': ['Versioned']} })
    OID: str = Field(default=..., description="""Local identifier within this study/context. Use CDISC OID format for regulatory submissions, or simple strings for internal use.""", json_schema_extra = { "linkml_meta": {'alias': 'OID', 'domain_of': ['Identifiable']} })
    uuid: Optional[str] = Field(default=None, description="""Universal unique identifier""", json_schema_extra = { "linkml_meta": {'alias': 'uuid', 'domain_of': ['Identifiable']} })
    name: Optional[str] = Field(default=None, description="""Short name or identifier, used for field names""", json_schema_extra = { "linkml_meta": {'alias': 'name', 'domain_of': ['Labelled', 'Standard']} })
    description: Optional[Union[TranslatedText, str]] = Field(default=None, description="""Detailed description, shown in tooltips""", json_schema_extra = { "linkml_meta": {'alias': 'description',
         'any_of': [{'range': 'string'}, {'range': 'TranslatedText'}],
         'domain_of': ['Labelled', 'CodeListItem']} })
    coding: Optional[list[Coding]] = Field(default=None, description="""Semantic tags for this element""", json_schema_extra = { "linkml_meta": {'alias': 'coding', 'domain_of': ['Labelled', 'CodeListItem', 'SourceItem']} })
    label: Optional[Union[TranslatedText, str]] = Field(default=None, description="""Human-readable label, shown in UIs""", json_schema_extra = { "linkml_meta": {'alias': 'label',
         'any_of': [{'range': 'string'}, {'range': 'TranslatedText'}],
         'domain_of': ['Labelled'],
         'exact_mappings': ['skos:prefLabel']} })
    aliases: Optional[list[Union[TranslatedText, str]]] = Field(default=None, description="""Alternative name or identifier""", json_schema_extra = { "linkml_meta": {'alias': 'aliases',
         'any_of': [{'range': 'string'}, {'range': 'TranslatedText'}],
         'domain_of': ['Labelled', 'CodeListItem'],
         'exact_mappings': ['skos:altLabel']} })
    mandatory: Optional[bool] = Field(default=None, description="""Is this element required?""", json_schema_extra = { "linkml_meta": {'alias': 'mandatory', 'domain_of': ['Governed']} })
    comments: Optional[list[str]] = Field(default=None, description="""Comment on the element, such as a rationale for its inclusion or exclusion""", json_schema_extra = { "linkml_meta": {'alias': 'comments', 'domain_of': ['Governed']} })
    siteOrSponsorComments: Optional[list[str]] = Field(default=None, description="""Comment on the element, such as a rationale for its inclusion or exclusion""", json_schema_extra = { "linkml_meta": {'alias': 'siteOrSponsorComments', 'domain_of': ['Governed']} })
    purpose: Optional[Union[TranslatedText, str]] = Field(default=None, description="""Purpose or rationale for this data element""", json_schema_extra = { "linkml_meta": {'alias': 'purpose',
         'any_of': [{'range': 'string'}, {'range': 'TranslatedText'}],
         'domain_of': ['Governed']} })
    lastUpdated: Optional[datetime ] = Field(default=None, description="""When the resource was last updated""", json_schema_extra = { "linkml_meta": {'alias': 'lastUpdated', 'domain_of': ['Governed']} })
    owner: Optional[str] = Field(default=None, description="""Party responsible for this element""", json_schema_extra = { "linkml_meta": {'alias': 'owner',
         'any_of': [{'range': 'User'}, {'range': 'Organization'}, {'range': 'string'}],
         'domain_of': ['Governed'],
         'narrow_mappings': ['prov:wasAttributedTo', 'prov:wasAssociatedBy']} })
    wasDerivedFrom: Optional[str] = Field(default=None, description="""Reference to another item that this item implements or extends, e.g. a template Item definition.""", json_schema_extra = { "linkml_meta": {'alias': 'wasDerivedFrom',
         'any_of': [{'range': 'Item'},
                    {'range': 'ItemGroup'},
                    {'range': 'MetaDataVersion'},
                    {'range': 'CodeList'},
                    {'range': 'ReifiedConcept'},
                    {'range': 'ConceptProperty'},
                    {'range': 'Condition'},
                    {'range': 'Method'},
                    {'range': 'NominalOccurrence'},
                    {'range': 'Dataflow'},
                    {'range': 'CubeComponent'},
                    {'range': 'DataProduct'},
                    {'range': 'ProvisionAgreement'}],
         'domain_of': ['Governed'],
         'exact_mappings': ['prov:wasDerivedFrom']} })


class IsSdmxDataset(ConfiguredBaseModel):
    """
    A mixin that provides additional metadata specific to SDMX Datasets
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://cdisc.org/define-json', 'mixin': True})

    action: Optional[str] = Field(default=None, description="""Defines the action to be taken by the recipient system (information, append, replace, delete)""", json_schema_extra = { "linkml_meta": {'alias': 'action', 'domain_of': ['IsSdmxDataset']} })
    reportingBegin: Optional[str] = Field(default=None, description="""A specific time period in a known system of time periods that identifies the start period of a report.""", json_schema_extra = { "linkml_meta": {'alias': 'reportingBegin', 'domain_of': ['IsSdmxDataset']} })
    reportingEnd: Optional[str] = Field(default=None, description="""A specific time period in a known system of time periods that identifies the end period of a report.""", json_schema_extra = { "linkml_meta": {'alias': 'reportingEnd', 'domain_of': ['IsSdmxDataset']} })
    dataExtractionDate: Optional[str] = Field(default=None, description="""A specific time period that identifies the date and time that the data are extracted from a data source.""", json_schema_extra = { "linkml_meta": {'alias': 'dataExtractionDate', 'domain_of': ['IsSdmxDataset']} })
    validFrom: Optional[str] = Field(default=None, description="""Indicates the inclusive start time indicating the validity of the information in the data set.""", json_schema_extra = { "linkml_meta": {'alias': 'validFrom', 'domain_of': ['IsSdmxDataset']} })
    validTo: Optional[str] = Field(default=None, description="""Indicates the inclusive end time indicating the validity of the information in the data set.""", json_schema_extra = { "linkml_meta": {'alias': 'validTo', 'domain_of': ['IsSdmxDataset']} })
    publicationYear: Optional[str] = Field(default=None, description="""Specifies the year of publication of the data or metadata in terms of whatever provisioning agreements might be in force.""", json_schema_extra = { "linkml_meta": {'alias': 'publicationYear', 'domain_of': ['IsSdmxDataset']} })
    publicationPeriod: Optional[str] = Field(default=None, description="""Specifies the period of publication of the data or metadata in terms of whatever provisioning agreements might be in force.""", json_schema_extra = { "linkml_meta": {'alias': 'publicationPeriod', 'domain_of': ['IsSdmxDataset']} })


class Dataset(IsSdmxDataset, IsProfile, Versioned, IdentifiableElement):
    """
    A collection element that groups observations sharing the same dimensionality, expressed as a set of unique dimensions within a Data Product context
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'close_mappings': ['qb:Dataset',
                            'sdmx:Dataset',
                            'dprod:Dataset',
                            'dcat:Dataset'],
         'from_schema': 'https://cdisc.org/define-json',
         'mixins': ['Versioned', 'IsProfile', 'IsSdmxDataset'],
         'narrow_mappings': ['sdmx:JsonDataset',
                             'sdmx:CsvDataset',
                             'sdmx:StructureSpecificDataset']})

    describedBy: Optional[str] = Field(default=None, description="""Associates a Dataflow and thereby a Data Structure Definition to the data set.""", json_schema_extra = { "linkml_meta": {'alias': 'describedBy', 'domain_of': ['Dataset', 'DatasetKey']} })
    structuredBy: Optional[str] = Field(default=None, description="""Associates the Data Structure Definition that defines the structure of the Data Set. Note that the Data Structure Definition is the same as that associated (non-mandatory) to the Dataflow.""", json_schema_extra = { "linkml_meta": {'alias': 'structuredBy', 'domain_of': ['Dataset']} })
    publishedBy: Optional[str] = Field(default=None, description="""Associates the Data Provider that reports/publishes the data.""", json_schema_extra = { "linkml_meta": {'alias': 'publishedBy',
         'any_of': [{'range': 'Organization'}, {'range': 'string'}],
         'domain_of': ['Dictionary', 'Dataset']} })
    keys: list[Union[GroupKey, SeriesKey]] = Field(default=..., description="""Series and Group keys in the data that are associated with dimensions in this structure""", json_schema_extra = { "linkml_meta": {'alias': 'keys',
         'any_of': [{'range': 'SeriesKey'}, {'range': 'GroupKey'}],
         'domain_of': ['Dataset']} })
    datasetType: Optional[str] = Field(default=None, description="""Type or classification of the dataset""", json_schema_extra = { "linkml_meta": {'alias': 'datasetType', 'domain_of': ['Dataset']} })
    distribution: Optional[list[Distribution]] = Field(default=None, description="""Representations of this dataset in various formats or access methods""", json_schema_extra = { "linkml_meta": {'alias': 'distribution',
         'domain_of': ['Dataset'],
         'exact_mappings': ['dcat:distribution']} })
    conformsTo: Optional[str] = Field(default=None, description="""Specification or standard that this dataset conforms to""", json_schema_extra = { "linkml_meta": {'alias': 'conformsTo',
         'close_mappings': ['dct:conformsTo'],
         'domain_of': ['Dataset', 'Distribution']} })
    hasPolicy: Optional[list[str]] = Field(default=None, description="""Access or usage policy applied to this dataset""", json_schema_extra = { "linkml_meta": {'alias': 'hasPolicy', 'domain_of': ['Dataset', 'DataProduct']} })
    informationSensitivityClassification: Optional[str] = Field(default=None, description="""Classification of the dataset's sensitivity or confidentiality""", json_schema_extra = { "linkml_meta": {'alias': 'informationSensitivityClassification', 'domain_of': ['Dataset']} })
    version: Optional[str] = Field(default=None, description="""The version of the external resources""", json_schema_extra = { "linkml_meta": {'alias': 'version', 'domain_of': ['Versioned', 'Standard']} })
    href: Optional[str] = Field(default=None, description="""Machine-readable instructions to obtain the resource e.g. FHIR path, URL""", json_schema_extra = { "linkml_meta": {'alias': 'href', 'domain_of': ['Versioned']} })
    profile: Optional[list[str]] = Field(default=None, description="""Profiles this resource claims to conform to""", json_schema_extra = { "linkml_meta": {'alias': 'profile', 'domain_of': ['IsProfile']} })
    security: Optional[list[Coding]] = Field(default=None, description="""Security tags applied to this resource""", json_schema_extra = { "linkml_meta": {'alias': 'security', 'domain_of': ['IsProfile']} })
    authenticator: Optional[str] = Field(default=None, description="""Who/what authenticated the resource""", json_schema_extra = { "linkml_meta": {'alias': 'authenticator',
         'any_of': [{'range': 'User'}, {'range': 'Organization'}, {'range': 'string'}],
         'domain_of': ['IsProfile']} })
    validityPeriod: Optional[str] = Field(default=None, description="""Time period during which the resouce is valid""", json_schema_extra = { "linkml_meta": {'alias': 'validityPeriod', 'domain_of': ['IsProfile']} })
    action: Optional[str] = Field(default=None, description="""Defines the action to be taken by the recipient system (information, append, replace, delete)""", json_schema_extra = { "linkml_meta": {'alias': 'action', 'domain_of': ['IsSdmxDataset']} })
    reportingBegin: Optional[str] = Field(default=None, description="""A specific time period in a known system of time periods that identifies the start period of a report.""", json_schema_extra = { "linkml_meta": {'alias': 'reportingBegin', 'domain_of': ['IsSdmxDataset']} })
    reportingEnd: Optional[str] = Field(default=None, description="""A specific time period in a known system of time periods that identifies the end period of a report.""", json_schema_extra = { "linkml_meta": {'alias': 'reportingEnd', 'domain_of': ['IsSdmxDataset']} })
    dataExtractionDate: Optional[str] = Field(default=None, description="""A specific time period that identifies the date and time that the data are extracted from a data source.""", json_schema_extra = { "linkml_meta": {'alias': 'dataExtractionDate', 'domain_of': ['IsSdmxDataset']} })
    validFrom: Optional[str] = Field(default=None, description="""Indicates the inclusive start time indicating the validity of the information in the data set.""", json_schema_extra = { "linkml_meta": {'alias': 'validFrom', 'domain_of': ['IsSdmxDataset']} })
    validTo: Optional[str] = Field(default=None, description="""Indicates the inclusive end time indicating the validity of the information in the data set.""", json_schema_extra = { "linkml_meta": {'alias': 'validTo', 'domain_of': ['IsSdmxDataset']} })
    publicationYear: Optional[str] = Field(default=None, description="""Specifies the year of publication of the data or metadata in terms of whatever provisioning agreements might be in force.""", json_schema_extra = { "linkml_meta": {'alias': 'publicationYear', 'domain_of': ['IsSdmxDataset']} })
    publicationPeriod: Optional[str] = Field(default=None, description="""Specifies the period of publication of the data or metadata in terms of whatever provisioning agreements might be in force.""", json_schema_extra = { "linkml_meta": {'alias': 'publicationPeriod', 'domain_of': ['IsSdmxDataset']} })
    OID: str = Field(default=..., description="""Local identifier within this study/context. Use CDISC OID format for regulatory submissions, or simple strings for internal use.""", json_schema_extra = { "linkml_meta": {'alias': 'OID', 'domain_of': ['Identifiable']} })
    uuid: Optional[str] = Field(default=None, description="""Universal unique identifier""", json_schema_extra = { "linkml_meta": {'alias': 'uuid', 'domain_of': ['Identifiable']} })
    name: Optional[str] = Field(default=None, description="""Short name or identifier, used for field names""", json_schema_extra = { "linkml_meta": {'alias': 'name', 'domain_of': ['Labelled', 'Standard']} })
    description: Optional[Union[TranslatedText, str]] = Field(default=None, description="""Detailed description, shown in tooltips""", json_schema_extra = { "linkml_meta": {'alias': 'description',
         'any_of': [{'range': 'string'}, {'range': 'TranslatedText'}],
         'domain_of': ['Labelled', 'CodeListItem']} })
    coding: Optional[list[Coding]] = Field(default=None, description="""Semantic tags for this element""", json_schema_extra = { "linkml_meta": {'alias': 'coding', 'domain_of': ['Labelled', 'CodeListItem', 'SourceItem']} })
    label: Optional[Union[TranslatedText, str]] = Field(default=None, description="""Human-readable label, shown in UIs""", json_schema_extra = { "linkml_meta": {'alias': 'label',
         'any_of': [{'range': 'string'}, {'range': 'TranslatedText'}],
         'domain_of': ['Labelled'],
         'exact_mappings': ['skos:prefLabel']} })
    aliases: Optional[list[Union[TranslatedText, str]]] = Field(default=None, description="""Alternative name or identifier""", json_schema_extra = { "linkml_meta": {'alias': 'aliases',
         'any_of': [{'range': 'string'}, {'range': 'TranslatedText'}],
         'domain_of': ['Labelled', 'CodeListItem'],
         'exact_mappings': ['skos:altLabel']} })


class DatasetKey(ConfiguredBaseModel):
    """
    An abstract identifier that comprises the cross-product of dimension values to identify a specific cross-section
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'abstract': True,
         'exact_mappings': ['sdmx:Key'],
         'from_schema': 'https://cdisc.org/define-json'})

    describedBy: Optional[str] = Field(default=None, description="""Associates the Dimension Descriptor defined in the Data Structure Definition""", json_schema_extra = { "linkml_meta": {'alias': 'describedBy',
         'any_of': [{'range': 'Dimension'}, {'range': 'ComponentList'}],
         'domain_of': ['Dataset', 'DatasetKey']} })
    keyValues: Optional[str] = Field(default=None, description="""List of Key Values that comprise each key, separated by a dot e.g. SUBJ001.VISIT2.BMI""", json_schema_extra = { "linkml_meta": {'alias': 'keyValues', 'domain_of': ['DatasetKey']} })
    attributeValues: Optional[str] = Field(default=None, description="""Association to the Attribute Values relating to Key""", json_schema_extra = { "linkml_meta": {'alias': 'attributeValues', 'domain_of': ['DatasetKey']} })


class GroupKey(DatasetKey):
    """
    A dimension subset that represents collections of dimensions that are subsets of the full dimension set, distinct from SeriesKey which includes Time dimensions
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'exact_mappings': ['sdmx:GroupKey'],
         'from_schema': 'https://cdisc.org/define-json'})

    describedBy: Optional[str] = Field(default=None, description="""Associates the Dimension Descriptor defined in the Data Structure Definition""", json_schema_extra = { "linkml_meta": {'alias': 'describedBy',
         'any_of': [{'range': 'Dimension'}, {'range': 'ComponentList'}],
         'domain_of': ['Dataset', 'DatasetKey']} })
    keyValues: Optional[str] = Field(default=None, description="""List of Key Values that comprise each key, separated by a dot e.g. SUBJ001.VISIT2.BMI""", json_schema_extra = { "linkml_meta": {'alias': 'keyValues', 'domain_of': ['DatasetKey']} })
    attributeValues: Optional[str] = Field(default=None, description="""Association to the Attribute Values relating to Key""", json_schema_extra = { "linkml_meta": {'alias': 'attributeValues', 'domain_of': ['DatasetKey']} })


class SeriesKey(DatasetKey):
    """
    A unique identifier that comprises the cross-product of dimension values including Time to identify observations, representing dimensions shared by all observations in a conceptual series
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'exact_mappings': ['sdmx:SeriesKey'],
         'from_schema': 'https://cdisc.org/define-json'})

    describedBy: Optional[str] = Field(default=None, description="""Associates the Dimension Descriptor defined in the Data Structure Definition""", json_schema_extra = { "linkml_meta": {'alias': 'describedBy',
         'any_of': [{'range': 'Dimension'}, {'range': 'ComponentList'}],
         'domain_of': ['Dataset', 'DatasetKey']} })
    keyValues: Optional[str] = Field(default=None, description="""List of Key Values that comprise each key, separated by a dot e.g. SUBJ001.VISIT2.BMI""", json_schema_extra = { "linkml_meta": {'alias': 'keyValues', 'domain_of': ['DatasetKey']} })
    attributeValues: Optional[str] = Field(default=None, description="""Association to the Attribute Values relating to Key""", json_schema_extra = { "linkml_meta": {'alias': 'attributeValues', 'domain_of': ['DatasetKey']} })


class CubeComponent(GovernedElement):
    """
    An abstract data field that represents a component in a data structure definition, referencing an Item for its definition
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'abstract': True,
         'exact_mappings': ['sdmx:Component'],
         'from_schema': 'https://cdisc.org/define-json'})

    item: str = Field(default=..., description="""Reference to the Item that defines this component's data structure and properties""", json_schema_extra = { "linkml_meta": {'alias': 'item',
         'domain_of': ['RangeCheck',
                       'SourceItem',
                       'CubeComponent',
                       'ObservationRelationship']} })
    role: Optional[str] = Field(default=None, description="""The role this component plays in its Structure Definition""", json_schema_extra = { "linkml_meta": {'alias': 'role', 'domain_of': ['IsODMItem', 'Organization', 'CubeComponent']} })
    missingHandling: Optional[str] = Field(default=None, description="""The method for handling missing values in the measure property""", json_schema_extra = { "linkml_meta": {'alias': 'missingHandling', 'domain_of': ['CubeComponent']} })
    imputation: Optional[str] = Field(default=None, description="""The imputation method used for the measure property""", json_schema_extra = { "linkml_meta": {'alias': 'imputation', 'domain_of': ['Timing', 'CubeComponent']} })
    OID: str = Field(default=..., description="""Local identifier within this study/context. Use CDISC OID format for regulatory submissions, or simple strings for internal use.""", json_schema_extra = { "linkml_meta": {'alias': 'OID', 'domain_of': ['Identifiable']} })
    uuid: Optional[str] = Field(default=None, description="""Universal unique identifier""", json_schema_extra = { "linkml_meta": {'alias': 'uuid', 'domain_of': ['Identifiable']} })
    name: Optional[str] = Field(default=None, description="""Short name or identifier, used for field names""", json_schema_extra = { "linkml_meta": {'alias': 'name', 'domain_of': ['Labelled', 'Standard']} })
    description: Optional[Union[TranslatedText, str]] = Field(default=None, description="""Detailed description, shown in tooltips""", json_schema_extra = { "linkml_meta": {'alias': 'description',
         'any_of': [{'range': 'string'}, {'range': 'TranslatedText'}],
         'domain_of': ['Labelled', 'CodeListItem']} })
    coding: Optional[list[Coding]] = Field(default=None, description="""Semantic tags for this element""", json_schema_extra = { "linkml_meta": {'alias': 'coding', 'domain_of': ['Labelled', 'CodeListItem', 'SourceItem']} })
    label: Optional[Union[TranslatedText, str]] = Field(default=None, description="""Human-readable label, shown in UIs""", json_schema_extra = { "linkml_meta": {'alias': 'label',
         'any_of': [{'range': 'string'}, {'range': 'TranslatedText'}],
         'domain_of': ['Labelled'],
         'exact_mappings': ['skos:prefLabel']} })
    aliases: Optional[list[Union[TranslatedText, str]]] = Field(default=None, description="""Alternative name or identifier""", json_schema_extra = { "linkml_meta": {'alias': 'aliases',
         'any_of': [{'range': 'string'}, {'range': 'TranslatedText'}],
         'domain_of': ['Labelled', 'CodeListItem'],
         'exact_mappings': ['skos:altLabel']} })
    mandatory: Optional[bool] = Field(default=None, description="""Is this element required?""", json_schema_extra = { "linkml_meta": {'alias': 'mandatory', 'domain_of': ['Governed']} })
    comments: Optional[list[str]] = Field(default=None, description="""Comment on the element, such as a rationale for its inclusion or exclusion""", json_schema_extra = { "linkml_meta": {'alias': 'comments', 'domain_of': ['Governed']} })
    siteOrSponsorComments: Optional[list[str]] = Field(default=None, description="""Comment on the element, such as a rationale for its inclusion or exclusion""", json_schema_extra = { "linkml_meta": {'alias': 'siteOrSponsorComments', 'domain_of': ['Governed']} })
    purpose: Optional[Union[TranslatedText, str]] = Field(default=None, description="""Purpose or rationale for this data element""", json_schema_extra = { "linkml_meta": {'alias': 'purpose',
         'any_of': [{'range': 'string'}, {'range': 'TranslatedText'}],
         'domain_of': ['Governed']} })
    lastUpdated: Optional[datetime ] = Field(default=None, description="""When the resource was last updated""", json_schema_extra = { "linkml_meta": {'alias': 'lastUpdated', 'domain_of': ['Governed']} })
    owner: Optional[str] = Field(default=None, description="""Party responsible for this element""", json_schema_extra = { "linkml_meta": {'alias': 'owner',
         'any_of': [{'range': 'User'}, {'range': 'Organization'}, {'range': 'string'}],
         'domain_of': ['Governed'],
         'narrow_mappings': ['prov:wasAttributedTo', 'prov:wasAssociatedBy']} })
    wasDerivedFrom: Optional[str] = Field(default=None, description="""Reference to another item that this item implements or extends, e.g. a template Item definition.""", json_schema_extra = { "linkml_meta": {'alias': 'wasDerivedFrom',
         'any_of': [{'range': 'Item'},
                    {'range': 'ItemGroup'},
                    {'range': 'MetaDataVersion'},
                    {'range': 'CodeList'},
                    {'range': 'ReifiedConcept'},
                    {'range': 'ConceptProperty'},
                    {'range': 'Condition'},
                    {'range': 'Method'},
                    {'range': 'NominalOccurrence'},
                    {'range': 'Dataflow'},
                    {'range': 'CubeComponent'},
                    {'range': 'DataProduct'},
                    {'range': 'ProvisionAgreement'}],
         'domain_of': ['Governed'],
         'exact_mappings': ['prov:wasDerivedFrom']} })


class Measure(CubeComponent):
    """
    A data cube property that describes a measurable quantity or value
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'exact_mappings': ['qb:MeasureProperty', 'sdmx:Measure'],
         'from_schema': 'https://cdisc.org/define-json'})

    item: str = Field(default=..., description="""Reference to the Item that defines this component's data structure and properties""", json_schema_extra = { "linkml_meta": {'alias': 'item',
         'domain_of': ['RangeCheck',
                       'SourceItem',
                       'CubeComponent',
                       'ObservationRelationship']} })
    role: Optional[str] = Field(default=None, description="""The role this component plays in its Structure Definition""", json_schema_extra = { "linkml_meta": {'alias': 'role', 'domain_of': ['IsODMItem', 'Organization', 'CubeComponent']} })
    missingHandling: Optional[str] = Field(default=None, description="""The method for handling missing values in the measure property""", json_schema_extra = { "linkml_meta": {'alias': 'missingHandling', 'domain_of': ['CubeComponent']} })
    imputation: Optional[str] = Field(default=None, description="""The imputation method used for the measure property""", json_schema_extra = { "linkml_meta": {'alias': 'imputation', 'domain_of': ['Timing', 'CubeComponent']} })
    OID: str = Field(default=..., description="""Local identifier within this study/context. Use CDISC OID format for regulatory submissions, or simple strings for internal use.""", json_schema_extra = { "linkml_meta": {'alias': 'OID', 'domain_of': ['Identifiable']} })
    uuid: Optional[str] = Field(default=None, description="""Universal unique identifier""", json_schema_extra = { "linkml_meta": {'alias': 'uuid', 'domain_of': ['Identifiable']} })
    name: Optional[str] = Field(default=None, description="""Short name or identifier, used for field names""", json_schema_extra = { "linkml_meta": {'alias': 'name', 'domain_of': ['Labelled', 'Standard']} })
    description: Optional[Union[TranslatedText, str]] = Field(default=None, description="""Detailed description, shown in tooltips""", json_schema_extra = { "linkml_meta": {'alias': 'description',
         'any_of': [{'range': 'string'}, {'range': 'TranslatedText'}],
         'domain_of': ['Labelled', 'CodeListItem']} })
    coding: Optional[list[Coding]] = Field(default=None, description="""Semantic tags for this element""", json_schema_extra = { "linkml_meta": {'alias': 'coding', 'domain_of': ['Labelled', 'CodeListItem', 'SourceItem']} })
    label: Optional[Union[TranslatedText, str]] = Field(default=None, description="""Human-readable label, shown in UIs""", json_schema_extra = { "linkml_meta": {'alias': 'label',
         'any_of': [{'range': 'string'}, {'range': 'TranslatedText'}],
         'domain_of': ['Labelled'],
         'exact_mappings': ['skos:prefLabel']} })
    aliases: Optional[list[Union[TranslatedText, str]]] = Field(default=None, description="""Alternative name or identifier""", json_schema_extra = { "linkml_meta": {'alias': 'aliases',
         'any_of': [{'range': 'string'}, {'range': 'TranslatedText'}],
         'domain_of': ['Labelled', 'CodeListItem'],
         'exact_mappings': ['skos:altLabel']} })
    mandatory: Optional[bool] = Field(default=None, description="""Is this element required?""", json_schema_extra = { "linkml_meta": {'alias': 'mandatory', 'domain_of': ['Governed']} })
    comments: Optional[list[str]] = Field(default=None, description="""Comment on the element, such as a rationale for its inclusion or exclusion""", json_schema_extra = { "linkml_meta": {'alias': 'comments', 'domain_of': ['Governed']} })
    siteOrSponsorComments: Optional[list[str]] = Field(default=None, description="""Comment on the element, such as a rationale for its inclusion or exclusion""", json_schema_extra = { "linkml_meta": {'alias': 'siteOrSponsorComments', 'domain_of': ['Governed']} })
    purpose: Optional[Union[TranslatedText, str]] = Field(default=None, description="""Purpose or rationale for this data element""", json_schema_extra = { "linkml_meta": {'alias': 'purpose',
         'any_of': [{'range': 'string'}, {'range': 'TranslatedText'}],
         'domain_of': ['Governed']} })
    lastUpdated: Optional[datetime ] = Field(default=None, description="""When the resource was last updated""", json_schema_extra = { "linkml_meta": {'alias': 'lastUpdated', 'domain_of': ['Governed']} })
    owner: Optional[str] = Field(default=None, description="""Party responsible for this element""", json_schema_extra = { "linkml_meta": {'alias': 'owner',
         'any_of': [{'range': 'User'}, {'range': 'Organization'}, {'range': 'string'}],
         'domain_of': ['Governed'],
         'narrow_mappings': ['prov:wasAttributedTo', 'prov:wasAssociatedBy']} })
    wasDerivedFrom: Optional[str] = Field(default=None, description="""Reference to another item that this item implements or extends, e.g. a template Item definition.""", json_schema_extra = { "linkml_meta": {'alias': 'wasDerivedFrom',
         'any_of': [{'range': 'Item'},
                    {'range': 'ItemGroup'},
                    {'range': 'MetaDataVersion'},
                    {'range': 'CodeList'},
                    {'range': 'ReifiedConcept'},
                    {'range': 'ConceptProperty'},
                    {'range': 'Condition'},
                    {'range': 'Method'},
                    {'range': 'NominalOccurrence'},
                    {'range': 'Dataflow'},
                    {'range': 'CubeComponent'},
                    {'range': 'DataProduct'},
                    {'range': 'ProvisionAgreement'}],
         'domain_of': ['Governed'],
         'exact_mappings': ['prov:wasDerivedFrom']} })


class Dimension(CubeComponent):
    """
    A data cube property that describes a categorical or hierarchical dimension
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'broad_mappings': ['sdmx:DataAttribute'],
         'exact_mappings': ['qb:DimensionProperty', 'sdmx:Dimension'],
         'from_schema': 'https://cdisc.org/define-json',
         'narrow_mappings': ['sdmx:MeasureDimension', 'sdmx:TimeDimension']})

    item: str = Field(default=..., description="""Reference to the Item that defines this component's data structure and properties""", json_schema_extra = { "linkml_meta": {'alias': 'item',
         'domain_of': ['RangeCheck',
                       'SourceItem',
                       'CubeComponent',
                       'ObservationRelationship']} })
    role: Optional[str] = Field(default=None, description="""The role this component plays in its Structure Definition""", json_schema_extra = { "linkml_meta": {'alias': 'role', 'domain_of': ['IsODMItem', 'Organization', 'CubeComponent']} })
    missingHandling: Optional[str] = Field(default=None, description="""The method for handling missing values in the measure property""", json_schema_extra = { "linkml_meta": {'alias': 'missingHandling', 'domain_of': ['CubeComponent']} })
    imputation: Optional[str] = Field(default=None, description="""The imputation method used for the measure property""", json_schema_extra = { "linkml_meta": {'alias': 'imputation', 'domain_of': ['Timing', 'CubeComponent']} })
    OID: str = Field(default=..., description="""Local identifier within this study/context. Use CDISC OID format for regulatory submissions, or simple strings for internal use.""", json_schema_extra = { "linkml_meta": {'alias': 'OID', 'domain_of': ['Identifiable']} })
    uuid: Optional[str] = Field(default=None, description="""Universal unique identifier""", json_schema_extra = { "linkml_meta": {'alias': 'uuid', 'domain_of': ['Identifiable']} })
    name: Optional[str] = Field(default=None, description="""Short name or identifier, used for field names""", json_schema_extra = { "linkml_meta": {'alias': 'name', 'domain_of': ['Labelled', 'Standard']} })
    description: Optional[Union[TranslatedText, str]] = Field(default=None, description="""Detailed description, shown in tooltips""", json_schema_extra = { "linkml_meta": {'alias': 'description',
         'any_of': [{'range': 'string'}, {'range': 'TranslatedText'}],
         'domain_of': ['Labelled', 'CodeListItem']} })
    coding: Optional[list[Coding]] = Field(default=None, description="""Semantic tags for this element""", json_schema_extra = { "linkml_meta": {'alias': 'coding', 'domain_of': ['Labelled', 'CodeListItem', 'SourceItem']} })
    label: Optional[Union[TranslatedText, str]] = Field(default=None, description="""Human-readable label, shown in UIs""", json_schema_extra = { "linkml_meta": {'alias': 'label',
         'any_of': [{'range': 'string'}, {'range': 'TranslatedText'}],
         'domain_of': ['Labelled'],
         'exact_mappings': ['skos:prefLabel']} })
    aliases: Optional[list[Union[TranslatedText, str]]] = Field(default=None, description="""Alternative name or identifier""", json_schema_extra = { "linkml_meta": {'alias': 'aliases',
         'any_of': [{'range': 'string'}, {'range': 'TranslatedText'}],
         'domain_of': ['Labelled', 'CodeListItem'],
         'exact_mappings': ['skos:altLabel']} })
    mandatory: Optional[bool] = Field(default=None, description="""Is this element required?""", json_schema_extra = { "linkml_meta": {'alias': 'mandatory', 'domain_of': ['Governed']} })
    comments: Optional[list[str]] = Field(default=None, description="""Comment on the element, such as a rationale for its inclusion or exclusion""", json_schema_extra = { "linkml_meta": {'alias': 'comments', 'domain_of': ['Governed']} })
    siteOrSponsorComments: Optional[list[str]] = Field(default=None, description="""Comment on the element, such as a rationale for its inclusion or exclusion""", json_schema_extra = { "linkml_meta": {'alias': 'siteOrSponsorComments', 'domain_of': ['Governed']} })
    purpose: Optional[Union[TranslatedText, str]] = Field(default=None, description="""Purpose or rationale for this data element""", json_schema_extra = { "linkml_meta": {'alias': 'purpose',
         'any_of': [{'range': 'string'}, {'range': 'TranslatedText'}],
         'domain_of': ['Governed']} })
    lastUpdated: Optional[datetime ] = Field(default=None, description="""When the resource was last updated""", json_schema_extra = { "linkml_meta": {'alias': 'lastUpdated', 'domain_of': ['Governed']} })
    owner: Optional[str] = Field(default=None, description="""Party responsible for this element""", json_schema_extra = { "linkml_meta": {'alias': 'owner',
         'any_of': [{'range': 'User'}, {'range': 'Organization'}, {'range': 'string'}],
         'domain_of': ['Governed'],
         'narrow_mappings': ['prov:wasAttributedTo', 'prov:wasAssociatedBy']} })
    wasDerivedFrom: Optional[str] = Field(default=None, description="""Reference to another item that this item implements or extends, e.g. a template Item definition.""", json_schema_extra = { "linkml_meta": {'alias': 'wasDerivedFrom',
         'any_of': [{'range': 'Item'},
                    {'range': 'ItemGroup'},
                    {'range': 'MetaDataVersion'},
                    {'range': 'CodeList'},
                    {'range': 'ReifiedConcept'},
                    {'range': 'ConceptProperty'},
                    {'range': 'Condition'},
                    {'range': 'Method'},
                    {'range': 'NominalOccurrence'},
                    {'range': 'Dataflow'},
                    {'range': 'CubeComponent'},
                    {'range': 'DataProduct'},
                    {'range': 'ProvisionAgreement'}],
         'domain_of': ['Governed'],
         'exact_mappings': ['prov:wasDerivedFrom']} })


class DataAttribute(CubeComponent):
    """
    A data cube property that describes additional characteristics or metadata about observations
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'exact_mappings': ['qb:AttributeProperty', 'sdmx:DataAttribute'],
         'from_schema': 'https://cdisc.org/define-json'})

    item: str = Field(default=..., description="""Reference to the Item that defines this component's data structure and properties""", json_schema_extra = { "linkml_meta": {'alias': 'item',
         'domain_of': ['RangeCheck',
                       'SourceItem',
                       'CubeComponent',
                       'ObservationRelationship']} })
    role: Optional[str] = Field(default=None, description="""The role this component plays in its Structure Definition""", json_schema_extra = { "linkml_meta": {'alias': 'role', 'domain_of': ['IsODMItem', 'Organization', 'CubeComponent']} })
    missingHandling: Optional[str] = Field(default=None, description="""The method for handling missing values in the measure property""", json_schema_extra = { "linkml_meta": {'alias': 'missingHandling', 'domain_of': ['CubeComponent']} })
    imputation: Optional[str] = Field(default=None, description="""The imputation method used for the measure property""", json_schema_extra = { "linkml_meta": {'alias': 'imputation', 'domain_of': ['Timing', 'CubeComponent']} })
    OID: str = Field(default=..., description="""Local identifier within this study/context. Use CDISC OID format for regulatory submissions, or simple strings for internal use.""", json_schema_extra = { "linkml_meta": {'alias': 'OID', 'domain_of': ['Identifiable']} })
    uuid: Optional[str] = Field(default=None, description="""Universal unique identifier""", json_schema_extra = { "linkml_meta": {'alias': 'uuid', 'domain_of': ['Identifiable']} })
    name: Optional[str] = Field(default=None, description="""Short name or identifier, used for field names""", json_schema_extra = { "linkml_meta": {'alias': 'name', 'domain_of': ['Labelled', 'Standard']} })
    description: Optional[Union[TranslatedText, str]] = Field(default=None, description="""Detailed description, shown in tooltips""", json_schema_extra = { "linkml_meta": {'alias': 'description',
         'any_of': [{'range': 'string'}, {'range': 'TranslatedText'}],
         'domain_of': ['Labelled', 'CodeListItem']} })
    coding: Optional[list[Coding]] = Field(default=None, description="""Semantic tags for this element""", json_schema_extra = { "linkml_meta": {'alias': 'coding', 'domain_of': ['Labelled', 'CodeListItem', 'SourceItem']} })
    label: Optional[Union[TranslatedText, str]] = Field(default=None, description="""Human-readable label, shown in UIs""", json_schema_extra = { "linkml_meta": {'alias': 'label',
         'any_of': [{'range': 'string'}, {'range': 'TranslatedText'}],
         'domain_of': ['Labelled'],
         'exact_mappings': ['skos:prefLabel']} })
    aliases: Optional[list[Union[TranslatedText, str]]] = Field(default=None, description="""Alternative name or identifier""", json_schema_extra = { "linkml_meta": {'alias': 'aliases',
         'any_of': [{'range': 'string'}, {'range': 'TranslatedText'}],
         'domain_of': ['Labelled', 'CodeListItem'],
         'exact_mappings': ['skos:altLabel']} })
    mandatory: Optional[bool] = Field(default=None, description="""Is this element required?""", json_schema_extra = { "linkml_meta": {'alias': 'mandatory', 'domain_of': ['Governed']} })
    comments: Optional[list[str]] = Field(default=None, description="""Comment on the element, such as a rationale for its inclusion or exclusion""", json_schema_extra = { "linkml_meta": {'alias': 'comments', 'domain_of': ['Governed']} })
    siteOrSponsorComments: Optional[list[str]] = Field(default=None, description="""Comment on the element, such as a rationale for its inclusion or exclusion""", json_schema_extra = { "linkml_meta": {'alias': 'siteOrSponsorComments', 'domain_of': ['Governed']} })
    purpose: Optional[Union[TranslatedText, str]] = Field(default=None, description="""Purpose or rationale for this data element""", json_schema_extra = { "linkml_meta": {'alias': 'purpose',
         'any_of': [{'range': 'string'}, {'range': 'TranslatedText'}],
         'domain_of': ['Governed']} })
    lastUpdated: Optional[datetime ] = Field(default=None, description="""When the resource was last updated""", json_schema_extra = { "linkml_meta": {'alias': 'lastUpdated', 'domain_of': ['Governed']} })
    owner: Optional[str] = Field(default=None, description="""Party responsible for this element""", json_schema_extra = { "linkml_meta": {'alias': 'owner',
         'any_of': [{'range': 'User'}, {'range': 'Organization'}, {'range': 'string'}],
         'domain_of': ['Governed'],
         'narrow_mappings': ['prov:wasAttributedTo', 'prov:wasAssociatedBy']} })
    wasDerivedFrom: Optional[str] = Field(default=None, description="""Reference to another item that this item implements or extends, e.g. a template Item definition.""", json_schema_extra = { "linkml_meta": {'alias': 'wasDerivedFrom',
         'any_of': [{'range': 'Item'},
                    {'range': 'ItemGroup'},
                    {'range': 'MetaDataVersion'},
                    {'range': 'CodeList'},
                    {'range': 'ReifiedConcept'},
                    {'range': 'ConceptProperty'},
                    {'range': 'Condition'},
                    {'range': 'Method'},
                    {'range': 'NominalOccurrence'},
                    {'range': 'Dataflow'},
                    {'range': 'CubeComponent'},
                    {'range': 'DataProduct'},
                    {'range': 'ProvisionAgreement'}],
         'domain_of': ['Governed'],
         'exact_mappings': ['prov:wasDerivedFrom']} })


class ComponentList(IdentifiableElement):
    """
    An abstract definition that specifies a list of components within a data structure definition, including various descriptor types
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'exact_mappings': ['sdmx:ComponentList'],
         'from_schema': 'https://cdisc.org/define-json'})

    components: Optional[list[Union[DataAttribute, Dimension, Measure]]] = Field(default=None, description="""The components that make up this component list""", json_schema_extra = { "linkml_meta": {'alias': 'components',
         'any_of': [{'range': 'Measure'},
                    {'range': 'Dimension'},
                    {'range': 'DataAttribute'}],
         'domain_of': ['ComponentList']} })
    OID: str = Field(default=..., description="""Local identifier within this study/context. Use CDISC OID format for regulatory submissions, or simple strings for internal use.""", json_schema_extra = { "linkml_meta": {'alias': 'OID', 'domain_of': ['Identifiable']} })
    uuid: Optional[str] = Field(default=None, description="""Universal unique identifier""", json_schema_extra = { "linkml_meta": {'alias': 'uuid', 'domain_of': ['Identifiable']} })
    name: Optional[str] = Field(default=None, description="""Short name or identifier, used for field names""", json_schema_extra = { "linkml_meta": {'alias': 'name', 'domain_of': ['Labelled', 'Standard']} })
    description: Optional[Union[TranslatedText, str]] = Field(default=None, description="""Detailed description, shown in tooltips""", json_schema_extra = { "linkml_meta": {'alias': 'description',
         'any_of': [{'range': 'string'}, {'range': 'TranslatedText'}],
         'domain_of': ['Labelled', 'CodeListItem']} })
    coding: Optional[list[Coding]] = Field(default=None, description="""Semantic tags for this element""", json_schema_extra = { "linkml_meta": {'alias': 'coding', 'domain_of': ['Labelled', 'CodeListItem', 'SourceItem']} })
    label: Optional[Union[TranslatedText, str]] = Field(default=None, description="""Human-readable label, shown in UIs""", json_schema_extra = { "linkml_meta": {'alias': 'label',
         'any_of': [{'range': 'string'}, {'range': 'TranslatedText'}],
         'domain_of': ['Labelled'],
         'exact_mappings': ['skos:prefLabel']} })
    aliases: Optional[list[Union[TranslatedText, str]]] = Field(default=None, description="""Alternative name or identifier""", json_schema_extra = { "linkml_meta": {'alias': 'aliases',
         'any_of': [{'range': 'string'}, {'range': 'TranslatedText'}],
         'domain_of': ['Labelled', 'CodeListItem'],
         'exact_mappings': ['skos:altLabel']} })


class MeasureRelationship(ConfiguredBaseModel):
    """
    A relationship element that associates a DataAttribute with a Measure
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'exact_mappings': ['sdmx:MeasureRelationship'],
         'from_schema': 'https://cdisc.org/define-json'})

    measure: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'measure', 'domain_of': ['MeasureRelationship']} })
    attribute: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'attribute',
         'domain_of': ['Resource',
                       'MeasureRelationship',
                       'DataflowRelationship',
                       'GroupRelationship',
                       'DimensionRelationship',
                       'ObservationRelationship']} })


class DataflowRelationship(ConfiguredBaseModel):
    """
    A relationship element that associates a DataAttribute with a Dataflow, reported at the Dataset level
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'exact_mappings': ['sdmx:DataflowRelationship'],
         'from_schema': 'https://cdisc.org/define-json'})

    dataFlow: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'dataFlow',
         'domain_of': ['DataflowRelationship', 'ProvisionAgreement']} })
    attribute: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'attribute',
         'domain_of': ['Resource',
                       'MeasureRelationship',
                       'DataflowRelationship',
                       'GroupRelationship',
                       'DimensionRelationship',
                       'ObservationRelationship']} })


class GroupRelationship(ConfiguredBaseModel):
    """
    A relationship element that associates a DataAttribute with a set of Dimensions, used when attribute values vary based on all group dimension values
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'exact_mappings': ['sdmx:GroupRelationship'],
         'from_schema': 'https://cdisc.org/define-json'})

    groupKey: Optional[str] = Field(default=None, description="""Set of dimensions that this definition depends on""", json_schema_extra = { "linkml_meta": {'alias': 'groupKey',
         'domain_of': ['GroupRelationship', 'DimensionRelationship'],
         'exact_mappings': ['sdmx:GroupDimensionDescriptor']} })
    attribute: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'attribute',
         'domain_of': ['Resource',
                       'MeasureRelationship',
                       'DataflowRelationship',
                       'GroupRelationship',
                       'DimensionRelationship',
                       'ObservationRelationship']} })


class DimensionRelationship(ConfiguredBaseModel):
    """
    A relationship element that associates a DataAttribute with a specific Dimension at a specific level
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'exact_mappings': ['sdmx:DimensionRelationship'],
         'from_schema': 'https://cdisc.org/define-json'})

    dimensions: Optional[list[str]] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'dimensions',
         'domain_of': ['DataStructureDefinition', 'DimensionRelationship'],
         'exact_mappings': ['sdmx:DimensionDescriptor']} })
    groupKey: Optional[str] = Field(default=None, description="""Set of dimensions that this definition depends on""", json_schema_extra = { "linkml_meta": {'alias': 'groupKey',
         'domain_of': ['GroupRelationship', 'DimensionRelationship'],
         'exact_mappings': ['sdmx:GroupDimensionDescriptor']} })
    attribute: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'attribute',
         'domain_of': ['Resource',
                       'MeasureRelationship',
                       'DataflowRelationship',
                       'GroupRelationship',
                       'DimensionRelationship',
                       'ObservationRelationship']} })


class ObservationRelationship(ConfiguredBaseModel):
    """
    A relationship element that associates a DataAttribute with an Observation, allowing value-level Items to be reused across multiple different Views
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'exact_mappings': ['sdmx:ObservationRelationship'],
         'from_schema': 'https://cdisc.org/define-json'})

    item: Optional[str] = Field(default=None, description="""Reference to the Item in an observation context that this definition applies to. e.g. the SDTM Variable Specialisation for a given Biomedical Concept Property.""", json_schema_extra = { "linkml_meta": {'alias': 'item',
         'domain_of': ['RangeCheck',
                       'SourceItem',
                       'CubeComponent',
                       'ObservationRelationship'],
         'exact_mappings': ['sdmx:ObservationDescriptor']} })
    attribute: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'attribute',
         'domain_of': ['Resource',
                       'MeasureRelationship',
                       'DataflowRelationship',
                       'GroupRelationship',
                       'DimensionRelationship',
                       'ObservationRelationship']} })


class DataProduct(Versioned, GovernedElement):
    """
    A governed collection that represents a purpose-driven assembly of datasets and services with an owning team and lifecycle
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'exact_mappings': ['dprod:DataProduct', 'dcat:DataService'],
         'from_schema': 'https://cdisc.org/define-json',
         'mixins': ['Versioned']})

    dataProductOwner: Optional[str] = Field(default=None, description="""The person or team accountable for this data product""", json_schema_extra = { "linkml_meta": {'alias': 'dataProductOwner',
         'any_of': [{'range': 'User'}, {'range': 'Organization'}, {'range': 'string'}],
         'domain_of': ['DataProduct'],
         'exact_mappings': ['prov:wasAttributedTo']} })
    domain: Optional[str] = Field(default=None, description="""The functional domain or business area this product serves""", json_schema_extra = { "linkml_meta": {'alias': 'domain', 'domain_of': ['ItemGroup', 'DataProduct']} })
    lifecycleStatus: Optional[DataProductLifecycleStatus] = Field(default=None, description="""Current lifecycle status of the data product""", json_schema_extra = { "linkml_meta": {'alias': 'lifecycleStatus', 'domain_of': ['DataProduct']} })
    inputPort: Optional[list[DataService]] = Field(default=None, description="""Services that provide input into this data product""", json_schema_extra = { "linkml_meta": {'alias': 'inputPort', 'domain_of': ['DataProduct']} })
    outputPort: Optional[list[DataService]] = Field(default=None, description="""Services that expose output from this data product""", json_schema_extra = { "linkml_meta": {'alias': 'outputPort', 'domain_of': ['DataProduct']} })
    inputDataset: Optional[list[Dataset]] = Field(default=None, description="""Source datasets used by the data product""", json_schema_extra = { "linkml_meta": {'alias': 'inputDataset', 'domain_of': ['DataProduct']} })
    outputDataset: Optional[list[Dataset]] = Field(default=None, description="""Output datasets produced by the data product""", json_schema_extra = { "linkml_meta": {'alias': 'outputDataset', 'domain_of': ['DataProduct']} })
    hasPolicy: Optional[list[str]] = Field(default=None, description="""Policies governing the use and access of the data product""", json_schema_extra = { "linkml_meta": {'alias': 'hasPolicy', 'domain_of': ['Dataset', 'DataProduct']} })
    version: Optional[str] = Field(default=None, description="""The version of the external resources""", json_schema_extra = { "linkml_meta": {'alias': 'version', 'domain_of': ['Versioned', 'Standard']} })
    href: Optional[str] = Field(default=None, description="""Machine-readable instructions to obtain the resource e.g. FHIR path, URL""", json_schema_extra = { "linkml_meta": {'alias': 'href', 'domain_of': ['Versioned']} })
    OID: str = Field(default=..., description="""Local identifier within this study/context. Use CDISC OID format for regulatory submissions, or simple strings for internal use.""", json_schema_extra = { "linkml_meta": {'alias': 'OID', 'domain_of': ['Identifiable']} })
    uuid: Optional[str] = Field(default=None, description="""Universal unique identifier""", json_schema_extra = { "linkml_meta": {'alias': 'uuid', 'domain_of': ['Identifiable']} })
    name: Optional[str] = Field(default=None, description="""Short name or identifier, used for field names""", json_schema_extra = { "linkml_meta": {'alias': 'name', 'domain_of': ['Labelled', 'Standard']} })
    description: Optional[Union[TranslatedText, str]] = Field(default=None, description="""Detailed description, shown in tooltips""", json_schema_extra = { "linkml_meta": {'alias': 'description',
         'any_of': [{'range': 'string'}, {'range': 'TranslatedText'}],
         'domain_of': ['Labelled', 'CodeListItem']} })
    coding: Optional[list[Coding]] = Field(default=None, description="""Semantic tags for this element""", json_schema_extra = { "linkml_meta": {'alias': 'coding', 'domain_of': ['Labelled', 'CodeListItem', 'SourceItem']} })
    label: Optional[Union[TranslatedText, str]] = Field(default=None, description="""Human-readable label, shown in UIs""", json_schema_extra = { "linkml_meta": {'alias': 'label',
         'any_of': [{'range': 'string'}, {'range': 'TranslatedText'}],
         'domain_of': ['Labelled'],
         'exact_mappings': ['skos:prefLabel']} })
    aliases: Optional[list[Union[TranslatedText, str]]] = Field(default=None, description="""Alternative name or identifier""", json_schema_extra = { "linkml_meta": {'alias': 'aliases',
         'any_of': [{'range': 'string'}, {'range': 'TranslatedText'}],
         'domain_of': ['Labelled', 'CodeListItem'],
         'exact_mappings': ['skos:altLabel']} })
    mandatory: Optional[bool] = Field(default=None, description="""Is this element required?""", json_schema_extra = { "linkml_meta": {'alias': 'mandatory', 'domain_of': ['Governed']} })
    comments: Optional[list[str]] = Field(default=None, description="""Comment on the element, such as a rationale for its inclusion or exclusion""", json_schema_extra = { "linkml_meta": {'alias': 'comments', 'domain_of': ['Governed']} })
    siteOrSponsorComments: Optional[list[str]] = Field(default=None, description="""Comment on the element, such as a rationale for its inclusion or exclusion""", json_schema_extra = { "linkml_meta": {'alias': 'siteOrSponsorComments', 'domain_of': ['Governed']} })
    purpose: Optional[Union[TranslatedText, str]] = Field(default=None, description="""Purpose or rationale for this data element""", json_schema_extra = { "linkml_meta": {'alias': 'purpose',
         'any_of': [{'range': 'string'}, {'range': 'TranslatedText'}],
         'domain_of': ['Governed']} })
    lastUpdated: Optional[datetime ] = Field(default=None, description="""When the resource was last updated""", json_schema_extra = { "linkml_meta": {'alias': 'lastUpdated', 'domain_of': ['Governed']} })
    owner: Optional[str] = Field(default=None, description="""Party responsible for this element""", json_schema_extra = { "linkml_meta": {'alias': 'owner',
         'any_of': [{'range': 'User'}, {'range': 'Organization'}, {'range': 'string'}],
         'domain_of': ['Governed'],
         'narrow_mappings': ['prov:wasAttributedTo', 'prov:wasAssociatedBy']} })
    wasDerivedFrom: Optional[str] = Field(default=None, description="""Reference to another item that this item implements or extends, e.g. a template Item definition.""", json_schema_extra = { "linkml_meta": {'alias': 'wasDerivedFrom',
         'any_of': [{'range': 'Item'},
                    {'range': 'ItemGroup'},
                    {'range': 'MetaDataVersion'},
                    {'range': 'CodeList'},
                    {'range': 'ReifiedConcept'},
                    {'range': 'ConceptProperty'},
                    {'range': 'Condition'},
                    {'range': 'Method'},
                    {'range': 'NominalOccurrence'},
                    {'range': 'Dataflow'},
                    {'range': 'CubeComponent'},
                    {'range': 'DataProduct'},
                    {'range': 'ProvisionAgreement'}],
         'domain_of': ['Governed'],
         'exact_mappings': ['prov:wasDerivedFrom']} })


class Distribution(ConfiguredBaseModel):
    """
    A technical representation that provides a specific format or access method for a dataset
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'exact_mappings': ['dprod:Distribution', 'dcat:Distribution'],
         'from_schema': 'https://cdisc.org/define-json',
         'narrow_mappings': ['sdmx:JsonDataset',
                             'sdmx:CsvDataset',
                             'sdmx:StructureSpecificDataset']})

    accessService: Optional[str] = Field(default=None, description="""Service that provides access to this distribution""", json_schema_extra = { "linkml_meta": {'alias': 'accessService', 'domain_of': ['Distribution']} })
    conformsTo: Optional[str] = Field(default=None, description="""The standard or specification the distribution conforms to""", json_schema_extra = { "linkml_meta": {'alias': 'conformsTo',
         'any_of': [{'range': 'string'}, {'range': 'DataStructureDefinition'}],
         'domain_of': ['Dataset', 'Distribution']} })
    isDistributionOf: Optional[str] = Field(default=None, description="""Dataset this distribution represents""", json_schema_extra = { "linkml_meta": {'alias': 'isDistributionOf', 'domain_of': ['Distribution']} })
    format: Optional[str] = Field(default=None, description="""File format or serialization used in the distribution""", json_schema_extra = { "linkml_meta": {'alias': 'format', 'domain_of': ['Distribution']} })


class DataService(Resource):
    """
    A service element that provides an API or endpoint for serving or receiving data
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'exact_mappings': ['dprod:DataService', 'dcat:DataService'],
         'from_schema': 'https://cdisc.org/define-json'})

    isAccessServiceOf: Optional[Distribution] = Field(default=None, description="""Distribution(s) for which this service provides access""", json_schema_extra = { "linkml_meta": {'alias': 'isAccessServiceOf', 'domain_of': ['DataService']} })
    protocol: Optional[str] = Field(default=None, description="""Protocol used by the service (e.g., HTTPS, FTP)""", json_schema_extra = { "linkml_meta": {'alias': 'protocol', 'domain_of': ['DataService']} })
    securitySchemaType: Optional[str] = Field(default=None, description="""Security or authentication method used (e.g., OAuth2)""", json_schema_extra = { "linkml_meta": {'alias': 'securitySchemaType', 'domain_of': ['DataService']} })
    resourceType: Optional[str] = Field(default=None, description="""Type of resource (e.g.,  \"ODM\", \"HL7-FHIR\", \"HL7-CDA\", \"HL7-v2\", \"OpenEHR-extract\")""", json_schema_extra = { "linkml_meta": {'alias': 'resourceType', 'domain_of': ['Resource']} })
    attribute: Optional[str] = Field(default=None, description="""Field provided by the Name attribute where the data or information can be obtained. Examples are \"valueQuantity.value\" or \"valueQuantity.unit\".""", json_schema_extra = { "linkml_meta": {'alias': 'attribute',
         'domain_of': ['Resource',
                       'MeasureRelationship',
                       'DataflowRelationship',
                       'GroupRelationship',
                       'DimensionRelationship',
                       'ObservationRelationship']} })
    selection: Optional[list[FormalExpression]] = Field(default=None, description="""Machine-executable instructions for selecting data from the resource.""", json_schema_extra = { "linkml_meta": {'alias': 'selection', 'domain_of': ['Resource']} })
    version: Optional[str] = Field(default=None, description="""The version of the external resources""", json_schema_extra = { "linkml_meta": {'alias': 'version', 'domain_of': ['Versioned', 'Standard']} })
    href: Optional[str] = Field(default=None, description="""Machine-readable instructions to obtain the resource e.g. FHIR path, URL""", json_schema_extra = { "linkml_meta": {'alias': 'href', 'domain_of': ['Versioned']} })
    OID: str = Field(default=..., description="""Local identifier within this study/context. Use CDISC OID format for regulatory submissions, or simple strings for internal use.""", json_schema_extra = { "linkml_meta": {'alias': 'OID', 'domain_of': ['Identifiable']} })
    uuid: Optional[str] = Field(default=None, description="""Universal unique identifier""", json_schema_extra = { "linkml_meta": {'alias': 'uuid', 'domain_of': ['Identifiable']} })
    name: Optional[str] = Field(default=None, description="""Short name or identifier, used for field names""", json_schema_extra = { "linkml_meta": {'alias': 'name', 'domain_of': ['Labelled', 'Standard']} })
    description: Optional[Union[TranslatedText, str]] = Field(default=None, description="""Detailed description, shown in tooltips""", json_schema_extra = { "linkml_meta": {'alias': 'description',
         'any_of': [{'range': 'string'}, {'range': 'TranslatedText'}],
         'domain_of': ['Labelled', 'CodeListItem']} })
    coding: Optional[list[Coding]] = Field(default=None, description="""Semantic tags for this element""", json_schema_extra = { "linkml_meta": {'alias': 'coding', 'domain_of': ['Labelled', 'CodeListItem', 'SourceItem']} })
    label: Optional[Union[TranslatedText, str]] = Field(default=None, description="""Human-readable label, shown in UIs""", json_schema_extra = { "linkml_meta": {'alias': 'label',
         'any_of': [{'range': 'string'}, {'range': 'TranslatedText'}],
         'domain_of': ['Labelled'],
         'exact_mappings': ['skos:prefLabel']} })
    aliases: Optional[list[Union[TranslatedText, str]]] = Field(default=None, description="""Alternative name or identifier""", json_schema_extra = { "linkml_meta": {'alias': 'aliases',
         'any_of': [{'range': 'string'}, {'range': 'TranslatedText'}],
         'domain_of': ['Labelled', 'CodeListItem'],
         'exact_mappings': ['skos:altLabel']} })


class DataProvider(Organization):
    """
    An organization element that provides data to a Data Consumer, which can be a sponsor, site, or any other entity that supplies data
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'close_mappings': ['sdmx:DataProvider'],
         'from_schema': 'https://cdisc.org/define-json'})

    providesDataFor: Optional[list[str]] = Field(default=None, description="""The Dataflows that this provider supplies data for""", json_schema_extra = { "linkml_meta": {'alias': 'providesDataFor', 'domain_of': ['DataProvider']} })
    provisionAgreements: Optional[list[str]] = Field(default=None, description="""The ProvisionAgreements that this provider has with Data Consumers""", json_schema_extra = { "linkml_meta": {'alias': 'provisionAgreements', 'domain_of': ['DataProvider']} })
    source: Optional[list[str]] = Field(default=None, description="""Association to a data source""", json_schema_extra = { "linkml_meta": {'alias': 'source',
         'domain_of': ['Origin',
                       'SiteOrSponsorComment',
                       'DataProvider',
                       'ProvisionAgreement']} })
    role: Optional[str] = Field(default=None, description="""The role of the organization in the study.""", json_schema_extra = { "linkml_meta": {'alias': 'role', 'domain_of': ['IsODMItem', 'Organization', 'CubeComponent']} })
    type: Optional[OrganizationType] = Field(default=None, description="""The type of organization (e.g., site, sponsor, vendor).""", json_schema_extra = { "linkml_meta": {'alias': 'type',
         'domain_of': ['ItemGroup',
                       'Method',
                       'Origin',
                       'Organization',
                       'Standard',
                       'Timing']} })
    location: Optional[str] = Field(default=None, description="""The physical location of the organization.""", json_schema_extra = { "linkml_meta": {'alias': 'location', 'domain_of': ['Organization', 'Display']} })
    address: Optional[str] = Field(default=None, description="""The address of the organization.""", json_schema_extra = { "linkml_meta": {'alias': 'address', 'domain_of': ['Organization']} })
    partOfOrganization: Optional[str] = Field(default=None, description="""Reference to a parent organization if this organization is part of a larger entity.""", json_schema_extra = { "linkml_meta": {'alias': 'partOfOrganization', 'domain_of': ['Organization']} })
    OID: str = Field(default=..., description="""Local identifier within this study/context. Use CDISC OID format for regulatory submissions, or simple strings for internal use.""", json_schema_extra = { "linkml_meta": {'alias': 'OID', 'domain_of': ['Identifiable']} })
    uuid: Optional[str] = Field(default=None, description="""Universal unique identifier""", json_schema_extra = { "linkml_meta": {'alias': 'uuid', 'domain_of': ['Identifiable']} })
    name: Optional[str] = Field(default=None, description="""Short name or identifier, used for field names""", json_schema_extra = { "linkml_meta": {'alias': 'name', 'domain_of': ['Labelled', 'Standard']} })
    description: Optional[Union[TranslatedText, str]] = Field(default=None, description="""Detailed description, shown in tooltips""", json_schema_extra = { "linkml_meta": {'alias': 'description',
         'any_of': [{'range': 'string'}, {'range': 'TranslatedText'}],
         'domain_of': ['Labelled', 'CodeListItem']} })
    coding: Optional[list[Coding]] = Field(default=None, description="""Semantic tags for this element""", json_schema_extra = { "linkml_meta": {'alias': 'coding', 'domain_of': ['Labelled', 'CodeListItem', 'SourceItem']} })
    label: Optional[Union[TranslatedText, str]] = Field(default=None, description="""Human-readable label, shown in UIs""", json_schema_extra = { "linkml_meta": {'alias': 'label',
         'any_of': [{'range': 'string'}, {'range': 'TranslatedText'}],
         'domain_of': ['Labelled'],
         'exact_mappings': ['skos:prefLabel']} })
    aliases: Optional[list[Union[TranslatedText, str]]] = Field(default=None, description="""Alternative name or identifier""", json_schema_extra = { "linkml_meta": {'alias': 'aliases',
         'any_of': [{'range': 'string'}, {'range': 'TranslatedText'}],
         'domain_of': ['Labelled', 'CodeListItem'],
         'exact_mappings': ['skos:altLabel']} })


class ProvisionAgreement(Versioned, GovernedElement):
    """
    An agreement element that describes the contractual relationship between a Data Provider and a Data Consumer regarding data provision
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'close_mappings': ['sdmx:ProvisionAgreement'],
         'from_schema': 'https://cdisc.org/define-json',
         'mixins': ['Versioned']})

    provider: Optional[str] = Field(default=None, description="""The Data Provider that is part of this agreement""", json_schema_extra = { "linkml_meta": {'alias': 'provider', 'domain_of': ['ProvisionAgreement']} })
    dataFlow: Optional[str] = Field(default=None, description="""The Dataflow that is covered by this agreement""", json_schema_extra = { "linkml_meta": {'alias': 'dataFlow',
         'domain_of': ['DataflowRelationship', 'ProvisionAgreement']} })
    source: Optional[str] = Field(default=None, description="""The source of the data provided under this agreement""", json_schema_extra = { "linkml_meta": {'alias': 'source',
         'domain_of': ['Origin',
                       'SiteOrSponsorComment',
                       'DataProvider',
                       'ProvisionAgreement']} })
    version: Optional[str] = Field(default=None, description="""The version of the external resources""", json_schema_extra = { "linkml_meta": {'alias': 'version', 'domain_of': ['Versioned', 'Standard']} })
    href: Optional[str] = Field(default=None, description="""Machine-readable instructions to obtain the resource e.g. FHIR path, URL""", json_schema_extra = { "linkml_meta": {'alias': 'href', 'domain_of': ['Versioned']} })
    OID: str = Field(default=..., description="""Local identifier within this study/context. Use CDISC OID format for regulatory submissions, or simple strings for internal use.""", json_schema_extra = { "linkml_meta": {'alias': 'OID', 'domain_of': ['Identifiable']} })
    uuid: Optional[str] = Field(default=None, description="""Universal unique identifier""", json_schema_extra = { "linkml_meta": {'alias': 'uuid', 'domain_of': ['Identifiable']} })
    name: Optional[str] = Field(default=None, description="""Short name or identifier, used for field names""", json_schema_extra = { "linkml_meta": {'alias': 'name', 'domain_of': ['Labelled', 'Standard']} })
    description: Optional[Union[TranslatedText, str]] = Field(default=None, description="""Detailed description, shown in tooltips""", json_schema_extra = { "linkml_meta": {'alias': 'description',
         'any_of': [{'range': 'string'}, {'range': 'TranslatedText'}],
         'domain_of': ['Labelled', 'CodeListItem']} })
    coding: Optional[list[Coding]] = Field(default=None, description="""Semantic tags for this element""", json_schema_extra = { "linkml_meta": {'alias': 'coding', 'domain_of': ['Labelled', 'CodeListItem', 'SourceItem']} })
    label: Optional[Union[TranslatedText, str]] = Field(default=None, description="""Human-readable label, shown in UIs""", json_schema_extra = { "linkml_meta": {'alias': 'label',
         'any_of': [{'range': 'string'}, {'range': 'TranslatedText'}],
         'domain_of': ['Labelled'],
         'exact_mappings': ['skos:prefLabel']} })
    aliases: Optional[list[Union[TranslatedText, str]]] = Field(default=None, description="""Alternative name or identifier""", json_schema_extra = { "linkml_meta": {'alias': 'aliases',
         'any_of': [{'range': 'string'}, {'range': 'TranslatedText'}],
         'domain_of': ['Labelled', 'CodeListItem'],
         'exact_mappings': ['skos:altLabel']} })
    mandatory: Optional[bool] = Field(default=None, description="""Is this element required?""", json_schema_extra = { "linkml_meta": {'alias': 'mandatory', 'domain_of': ['Governed']} })
    comments: Optional[list[str]] = Field(default=None, description="""Comment on the element, such as a rationale for its inclusion or exclusion""", json_schema_extra = { "linkml_meta": {'alias': 'comments', 'domain_of': ['Governed']} })
    siteOrSponsorComments: Optional[list[str]] = Field(default=None, description="""Comment on the element, such as a rationale for its inclusion or exclusion""", json_schema_extra = { "linkml_meta": {'alias': 'siteOrSponsorComments', 'domain_of': ['Governed']} })
    purpose: Optional[Union[TranslatedText, str]] = Field(default=None, description="""Purpose or rationale for this data element""", json_schema_extra = { "linkml_meta": {'alias': 'purpose',
         'any_of': [{'range': 'string'}, {'range': 'TranslatedText'}],
         'domain_of': ['Governed']} })
    lastUpdated: Optional[datetime ] = Field(default=None, description="""When the resource was last updated""", json_schema_extra = { "linkml_meta": {'alias': 'lastUpdated', 'domain_of': ['Governed']} })
    owner: Optional[str] = Field(default=None, description="""Party responsible for this element""", json_schema_extra = { "linkml_meta": {'alias': 'owner',
         'any_of': [{'range': 'User'}, {'range': 'Organization'}, {'range': 'string'}],
         'domain_of': ['Governed'],
         'narrow_mappings': ['prov:wasAttributedTo', 'prov:wasAssociatedBy']} })
    wasDerivedFrom: Optional[str] = Field(default=None, description="""Reference to another item that this item implements or extends, e.g. a template Item definition.""", json_schema_extra = { "linkml_meta": {'alias': 'wasDerivedFrom',
         'any_of': [{'range': 'Item'},
                    {'range': 'ItemGroup'},
                    {'range': 'MetaDataVersion'},
                    {'range': 'CodeList'},
                    {'range': 'ReifiedConcept'},
                    {'range': 'ConceptProperty'},
                    {'range': 'Condition'},
                    {'range': 'Method'},
                    {'range': 'NominalOccurrence'},
                    {'range': 'Dataflow'},
                    {'range': 'CubeComponent'},
                    {'range': 'DataProduct'},
                    {'range': 'ProvisionAgreement'}],
         'domain_of': ['Governed'],
         'exact_mappings': ['prov:wasDerivedFrom']} })


class Analysis(Method, Versioned):
    """
    Analysis extends Method to capture analysis-specific metadata including the reason for analysis, its purpose, and data traceability for the results used.
    Expressions and parameters from Method can be generic or implementation-specific.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://cdisc.org/define-json', 'mixins': ['Versioned']})

    analysisReason: Optional[str] = Field(default=None, description="""The reason this analysis was performed.  """, json_schema_extra = { "linkml_meta": {'alias': 'analysisReason', 'domain_of': ['Analysis']} })
    analysisPurpose: Optional[str] = Field(default=None, description="""The purpose or role of this analysis in the study.""", json_schema_extra = { "linkml_meta": {'alias': 'analysisPurpose', 'domain_of': ['Analysis']} })
    analysisMethod: Optional[str] = Field(default=None, description="""Generic method used to perform this analysis. any_of:
  - range: Method
  - range: AnalysisMethod""", json_schema_extra = { "linkml_meta": {'alias': 'analysisMethod', 'domain_of': ['Dataflow', 'Analysis']} })
    applicableWhen: Optional[list[str]] = Field(default=None, description="""The conditions (e.g. population, time period etc.) that must be met for this analysis to be applicable.""", json_schema_extra = { "linkml_meta": {'alias': 'applicableWhen',
         'domain_of': ['Item', 'ItemGroup', 'Parameter', 'Analysis']} })
    inputData: Optional[list[str]] = Field(default=None, description="""Datasets or slices/subsets of datasets asked for by this analysis. If a Item is referenced by a Parameter e.g. Analysis Variable, make sure to include its parent ItemGroup here.""", json_schema_extra = { "linkml_meta": {'alias': 'inputData',
         'any_of': [{'range': 'ItemGroup'}, {'range': 'Dataset'}],
         'domain_of': ['Analysis']} })
    version: Optional[str] = Field(default=None, description="""The version of the external resources""", json_schema_extra = { "linkml_meta": {'alias': 'version', 'domain_of': ['Versioned', 'Standard']} })
    href: Optional[str] = Field(default=None, description="""Machine-readable instructions to obtain the resource e.g. FHIR path, URL""", json_schema_extra = { "linkml_meta": {'alias': 'href', 'domain_of': ['Versioned']} })
    type: Optional[MethodType] = Field(default=None, description="""The type of method e.g. Computation, Imputation, Transformation.""", json_schema_extra = { "linkml_meta": {'alias': 'type',
         'domain_of': ['ItemGroup',
                       'Method',
                       'Origin',
                       'Organization',
                       'Standard',
                       'Timing']} })
    expressions: Optional[list[FormalExpression]] = Field(default=None, description="""Formal expressions used by this method""", json_schema_extra = { "linkml_meta": {'alias': 'expressions', 'domain_of': ['Condition', 'RangeCheck', 'Method']} })
    documents: Optional[list[DocumentReference]] = Field(default=None, description="""Reference to a document that describes this method in detail.""", json_schema_extra = { "linkml_meta": {'alias': 'documents', 'domain_of': ['Comment', 'Method', 'Origin']} })
    implementsConcept: Optional[str] = Field(default=None, description="""Reference to a specific concept that this Method implements.""", json_schema_extra = { "linkml_meta": {'alias': 'implementsConcept', 'domain_of': ['ItemGroup', 'Method']} })
    OID: str = Field(default=..., description="""Local identifier within this study/context. Use CDISC OID format for regulatory submissions, or simple strings for internal use.""", json_schema_extra = { "linkml_meta": {'alias': 'OID', 'domain_of': ['Identifiable']} })
    uuid: Optional[str] = Field(default=None, description="""Universal unique identifier""", json_schema_extra = { "linkml_meta": {'alias': 'uuid', 'domain_of': ['Identifiable']} })
    name: Optional[str] = Field(default=None, description="""Short name or identifier, used for field names""", json_schema_extra = { "linkml_meta": {'alias': 'name', 'domain_of': ['Labelled', 'Standard']} })
    description: Optional[Union[TranslatedText, str]] = Field(default=None, description="""Detailed description, shown in tooltips""", json_schema_extra = { "linkml_meta": {'alias': 'description',
         'any_of': [{'range': 'string'}, {'range': 'TranslatedText'}],
         'domain_of': ['Labelled', 'CodeListItem']} })
    coding: Optional[list[Coding]] = Field(default=None, description="""Semantic tags for this element""", json_schema_extra = { "linkml_meta": {'alias': 'coding', 'domain_of': ['Labelled', 'CodeListItem', 'SourceItem']} })
    label: Optional[Union[TranslatedText, str]] = Field(default=None, description="""Human-readable label, shown in UIs""", json_schema_extra = { "linkml_meta": {'alias': 'label',
         'any_of': [{'range': 'string'}, {'range': 'TranslatedText'}],
         'domain_of': ['Labelled'],
         'exact_mappings': ['skos:prefLabel']} })
    aliases: Optional[list[Union[TranslatedText, str]]] = Field(default=None, description="""Alternative name or identifier""", json_schema_extra = { "linkml_meta": {'alias': 'aliases',
         'any_of': [{'range': 'string'}, {'range': 'TranslatedText'}],
         'domain_of': ['Labelled', 'CodeListItem'],
         'exact_mappings': ['skos:altLabel']} })
    mandatory: Optional[bool] = Field(default=None, description="""Is this element required?""", json_schema_extra = { "linkml_meta": {'alias': 'mandatory', 'domain_of': ['Governed']} })
    comments: Optional[list[str]] = Field(default=None, description="""Comment on the element, such as a rationale for its inclusion or exclusion""", json_schema_extra = { "linkml_meta": {'alias': 'comments', 'domain_of': ['Governed']} })
    siteOrSponsorComments: Optional[list[str]] = Field(default=None, description="""Comment on the element, such as a rationale for its inclusion or exclusion""", json_schema_extra = { "linkml_meta": {'alias': 'siteOrSponsorComments', 'domain_of': ['Governed']} })
    purpose: Optional[Union[TranslatedText, str]] = Field(default=None, description="""Purpose or rationale for this data element""", json_schema_extra = { "linkml_meta": {'alias': 'purpose',
         'any_of': [{'range': 'string'}, {'range': 'TranslatedText'}],
         'domain_of': ['Governed']} })
    lastUpdated: Optional[datetime ] = Field(default=None, description="""When the resource was last updated""", json_schema_extra = { "linkml_meta": {'alias': 'lastUpdated', 'domain_of': ['Governed']} })
    owner: Optional[str] = Field(default=None, description="""Party responsible for this element""", json_schema_extra = { "linkml_meta": {'alias': 'owner',
         'any_of': [{'range': 'User'}, {'range': 'Organization'}, {'range': 'string'}],
         'domain_of': ['Governed'],
         'narrow_mappings': ['prov:wasAttributedTo', 'prov:wasAssociatedBy']} })
    wasDerivedFrom: Optional[str] = Field(default=None, description="""Reference to another item that this item implements or extends, e.g. a template Item definition.""", json_schema_extra = { "linkml_meta": {'alias': 'wasDerivedFrom',
         'any_of': [{'range': 'Item'},
                    {'range': 'ItemGroup'},
                    {'range': 'MetaDataVersion'},
                    {'range': 'CodeList'},
                    {'range': 'ReifiedConcept'},
                    {'range': 'ConceptProperty'},
                    {'range': 'Condition'},
                    {'range': 'Method'},
                    {'range': 'NominalOccurrence'},
                    {'range': 'Dataflow'},
                    {'range': 'CubeComponent'},
                    {'range': 'DataProduct'},
                    {'range': 'ProvisionAgreement'}],
         'domain_of': ['Governed'],
         'exact_mappings': ['prov:wasDerivedFrom']} })


class Display(Versioned, GovernedElement):
    """
    A rendered output of an analysis result.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://cdisc.org/define-json', 'mixins': ['Versioned']})

    analysis: Optional[str] = Field(default=None, description="""Analysis result this display represents.""", json_schema_extra = { "linkml_meta": {'alias': 'analysis', 'domain_of': ['Display']} })
    displayType: Optional[str] = Field(default=None, description="""The type of display this result represents. e.g. table, listing, figure, dashboard.""", json_schema_extra = { "linkml_meta": {'alias': 'displayType', 'domain_of': ['Display']} })
    location: Optional[list[DocumentReference]] = Field(default=None, description="""Reference to documents / location containing the display.""", json_schema_extra = { "linkml_meta": {'alias': 'location', 'domain_of': ['Organization', 'Display']} })
    version: Optional[str] = Field(default=None, description="""The version of the external resources""", json_schema_extra = { "linkml_meta": {'alias': 'version', 'domain_of': ['Versioned', 'Standard']} })
    href: Optional[str] = Field(default=None, description="""Machine-readable instructions to obtain the resource e.g. FHIR path, URL""", json_schema_extra = { "linkml_meta": {'alias': 'href', 'domain_of': ['Versioned']} })
    OID: str = Field(default=..., description="""Local identifier within this study/context. Use CDISC OID format for regulatory submissions, or simple strings for internal use.""", json_schema_extra = { "linkml_meta": {'alias': 'OID', 'domain_of': ['Identifiable']} })
    uuid: Optional[str] = Field(default=None, description="""Universal unique identifier""", json_schema_extra = { "linkml_meta": {'alias': 'uuid', 'domain_of': ['Identifiable']} })
    name: Optional[str] = Field(default=None, description="""Short name or identifier, used for field names""", json_schema_extra = { "linkml_meta": {'alias': 'name', 'domain_of': ['Labelled', 'Standard']} })
    description: Optional[Union[TranslatedText, str]] = Field(default=None, description="""Detailed description, shown in tooltips""", json_schema_extra = { "linkml_meta": {'alias': 'description',
         'any_of': [{'range': 'string'}, {'range': 'TranslatedText'}],
         'domain_of': ['Labelled', 'CodeListItem']} })
    coding: Optional[list[Coding]] = Field(default=None, description="""Semantic tags for this element""", json_schema_extra = { "linkml_meta": {'alias': 'coding', 'domain_of': ['Labelled', 'CodeListItem', 'SourceItem']} })
    label: Optional[Union[TranslatedText, str]] = Field(default=None, description="""Human-readable label, shown in UIs""", json_schema_extra = { "linkml_meta": {'alias': 'label',
         'any_of': [{'range': 'string'}, {'range': 'TranslatedText'}],
         'domain_of': ['Labelled'],
         'exact_mappings': ['skos:prefLabel']} })
    aliases: Optional[list[Union[TranslatedText, str]]] = Field(default=None, description="""Alternative name or identifier""", json_schema_extra = { "linkml_meta": {'alias': 'aliases',
         'any_of': [{'range': 'string'}, {'range': 'TranslatedText'}],
         'domain_of': ['Labelled', 'CodeListItem'],
         'exact_mappings': ['skos:altLabel']} })
    mandatory: Optional[bool] = Field(default=None, description="""Is this element required?""", json_schema_extra = { "linkml_meta": {'alias': 'mandatory', 'domain_of': ['Governed']} })
    comments: Optional[list[str]] = Field(default=None, description="""Comment on the element, such as a rationale for its inclusion or exclusion""", json_schema_extra = { "linkml_meta": {'alias': 'comments', 'domain_of': ['Governed']} })
    siteOrSponsorComments: Optional[list[str]] = Field(default=None, description="""Comment on the element, such as a rationale for its inclusion or exclusion""", json_schema_extra = { "linkml_meta": {'alias': 'siteOrSponsorComments', 'domain_of': ['Governed']} })
    purpose: Optional[Union[TranslatedText, str]] = Field(default=None, description="""Purpose or rationale for this data element""", json_schema_extra = { "linkml_meta": {'alias': 'purpose',
         'any_of': [{'range': 'string'}, {'range': 'TranslatedText'}],
         'domain_of': ['Governed']} })
    lastUpdated: Optional[datetime ] = Field(default=None, description="""When the resource was last updated""", json_schema_extra = { "linkml_meta": {'alias': 'lastUpdated', 'domain_of': ['Governed']} })
    owner: Optional[str] = Field(default=None, description="""Party responsible for this element""", json_schema_extra = { "linkml_meta": {'alias': 'owner',
         'any_of': [{'range': 'User'}, {'range': 'Organization'}, {'range': 'string'}],
         'domain_of': ['Governed'],
         'narrow_mappings': ['prov:wasAttributedTo', 'prov:wasAssociatedBy']} })
    wasDerivedFrom: Optional[str] = Field(default=None, description="""Reference to another item that this item implements or extends, e.g. a template Item definition.""", json_schema_extra = { "linkml_meta": {'alias': 'wasDerivedFrom',
         'any_of': [{'range': 'Item'},
                    {'range': 'ItemGroup'},
                    {'range': 'MetaDataVersion'},
                    {'range': 'CodeList'},
                    {'range': 'ReifiedConcept'},
                    {'range': 'ConceptProperty'},
                    {'range': 'Condition'},
                    {'range': 'Method'},
                    {'range': 'NominalOccurrence'},
                    {'range': 'Dataflow'},
                    {'range': 'CubeComponent'},
                    {'range': 'DataProduct'},
                    {'range': 'ProvisionAgreement'}],
         'domain_of': ['Governed'],
         'exact_mappings': ['prov:wasDerivedFrom']} })


# Model rebuild
# see https://pydantic-docs.helpmanual.io/usage/models/#rebuilding-a-model
Identifiable.model_rebuild()
Governed.model_rebuild()
Labelled.model_rebuild()
IdentifiableElement.model_rebuild()
GovernedElement.model_rebuild()
Formatted.model_rebuild()
Versioned.model_rebuild()
IsProfile.model_rebuild()
IsODMItem.model_rebuild()
ODMFileMetadata.model_rebuild()
StudyMetadata.model_rebuild()
MetaDataVersion.model_rebuild()
Item.model_rebuild()
ItemGroup.model_rebuild()
Relationship.model_rebuild()
Translation.model_rebuild()
TranslatedText.model_rebuild()
CodeList.model_rebuild()
CodeListItem.model_rebuild()
Comment.model_rebuild()
Coding.model_rebuild()
Dictionary.model_rebuild()
ReifiedConcept.model_rebuild()
ConceptProperty.model_rebuild()
WhereClause.model_rebuild()
Condition.model_rebuild()
RangeCheck.model_rebuild()
FormalExpression.model_rebuild()
Method.model_rebuild()
SourceItem.model_rebuild()
Parameter.model_rebuild()
ReturnValue.model_rebuild()
Origin.model_rebuild()
SiteOrSponsorComment.model_rebuild()
User.model_rebuild()
Organization.model_rebuild()
Standard.model_rebuild()
Resource.model_rebuild()
DocumentReference.model_rebuild()
Timing.model_rebuild()
NominalOccurrence.model_rebuild()
DataStructureDefinition.model_rebuild()
Dataflow.model_rebuild()
IsSdmxDataset.model_rebuild()
Dataset.model_rebuild()
DatasetKey.model_rebuild()
GroupKey.model_rebuild()
SeriesKey.model_rebuild()
CubeComponent.model_rebuild()
Measure.model_rebuild()
Dimension.model_rebuild()
DataAttribute.model_rebuild()
ComponentList.model_rebuild()
MeasureRelationship.model_rebuild()
DataflowRelationship.model_rebuild()
GroupRelationship.model_rebuild()
DimensionRelationship.model_rebuild()
ObservationRelationship.model_rebuild()
DataProduct.model_rebuild()
Distribution.model_rebuild()
DataService.model_rebuild()
DataProvider.model_rebuild()
ProvisionAgreement.model_rebuild()
Analysis.model_rebuild()
Display.model_rebuild()

