from db.codes.business_size_code import BusinessSizeCode
from db.codes.beneficiary_size_code import BeneficiarySizeCode
from db.codes.cause_code import CauseCode
from db.codes.cause_preference_rank_code import CausePreferenceRankCode
from errors.error import Error

class RequestValidationHandler():
    def validate_params(self,params) -> []:
        errors = []
        if not params['user_id']:
            errors.append(
                Error.create_invalid_parameter_error("registration.user.id", "User Id required")
            )
        entity_type = params['entity_type']
        if not entity_type:
            errors.append(
                Error.create_invalid_parameter_error("registration.entityType", "entitityType is required")
            )
        else:
            if entity_type not in ('business, beneficiary'):
                errors.append(
                    Error.create_invalid_parameter_error("registration.entityType", f"Invalid entity type: {entity_type}")
                )
        if not params['name']:
            errors.append(
                Error.create_invalid_parameter_error("registration.profile.name", "name required")
            )
        if not params['email']:
            errors.append(
                Error.create_invalid_parameter_error("registration.profile.email", "email required")
            )
        # Validate phone_number
        # Validate website_url
        if not params["location_state"]:
            errors.append(
                Error.create_invalid_parameter_error("registration.profile.location.state", "state required")
            )
        elif len(params["location_state"]) != 2 or not self.is_valid_state(params["location_state"].upper()):
                errors.append(
                    Error.create_invalid_parameter_error("registration.profile.location.state", f"invalid state", params["location_state"])
                )
        if not params["location_city"]:
            errors.append(
                Error.create_invalid_parameter_error("registration.profile.location.city", "city required")
            )

        # size validation for business, beneficiary
        if (entity_type in ('business', 'beneficiary')):
            size = params['size']
            if not size:
                errors.append(
                    Error.create_invalid_parameter_error("registration.profile.size", "size required")
                )
            elif (entity_type == 'business' and not BusinessSizeCode.from_str(size)):
                errors.append(
                    Error.create_invalid_parameter_error("registration.profile.size", "unsupported business size", size)
                )    
            elif (entity_type == 'beneficiary' and not BeneficiarySizeCode.from_str(size)):
                errors.append(
                    Error.create_invalid_parameter_error("registration.profile.size", "unrecognized size", size)
                )
        
        # validate causes 
        # NOTE: this does not valid invalid object structure in request.
        # causes are represented as a list of objects with two values: name + rank
        causes = params['causes']

        # validate cause names and ranks
        invalid_causes: list[str] = None
        invalid_ranks: list[str] = None
        invalid_causes = [
                cause["name"] for cause in causes
                if CauseCode.from_str(cause["name"]) is None
            ]
        invalid_ranks = [
                cause["rank"] for cause in causes
                if CausePreferenceRankCode.from_str(cause["rank"]) is None
            ]
        
        if len(invalid_causes) > 0:
            invalid_cause_message = ",".join(invalid_causes)
            errors.append(
                Error.create_invalid_parameter_error(
                    field="registration.causePreferences", error_message=f"Invalid cause(s):", value=invalid_cause_message
                )
            )
        if len(invalid_ranks) > 0:
            invalid_rank_message = ",".join(invalid_ranks)
            errors.append(
                Error.create_invalid_parameter_error(
                    field="registration.causePreferences", error_message=f"Invalid rank(s):", value=invalid_rank_message
                )
            )

        # validate cause business-rules
        if entity_type == "business":
            if (len(causes) < 3):
                errors.append(
                    Error.create_invalid_parameter_error(
                        "registration.causes", f"minimum cause count: 3. found: {len(causes)}"
                    )
                )
            if sum(CausePreferenceRankCode.from_str(cause["rank"]) != CausePreferenceRankCode.UNRANKED for cause in causes):
                errors.append(
                    Error.create_invalid_parameter_error("registration.causePreferences", "Business registration does not support ranked causes")
                )
        elif entity_type == "beneficiary":
            primary_cause_count = sum(cause["rank"] == CausePreferenceRankCode.UNRANKED.name for cause in causes)
            supporting_cause_count = sum(cause["rank"] == CausePreferenceRankCode.SUPPORTING.name for cause in causes)
            unranked_cause_count = len(causes) != primary_cause_count + supporting_cause_count
            if primary_cause_count != 1:
                errors.append(
                    Error.create_invalid_parameter_error("registration.causePreferences", error_message=f"there must be exactly 1 cause with the 'PRIMARY' rank. found: {primary_cause_count}")
                )
            if supporting_cause_count > 2:
                errors.append(
                    Error.create_invalid_parameter_error("registration.causePreferences", error_message=f"there may only be up to 2 causes with the 'SUPPORTING' rank. found: {supporting_cause_count}")
                )
            if unranked_cause_count:
                errors.append(
                    Error.create_invalid_parameter_error("registration.causePreferences", error_message=f"causes must be ranked. unranked causes found: {unranked_cause_count}")
                )
        
        return errors

    def is_valid_state(self, state: str) -> bool:
        return state in [
            "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA", 
            "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", 
            "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
            "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
            "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"
        ]
