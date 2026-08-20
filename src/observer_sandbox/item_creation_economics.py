from __future__ import annotations


DEFAULT_ITEM_ECONOMIC_INSTRUCTION = (
    "ECONOMIC INVARIANT: ordinary real-world goods that can normally be bought, sold, or replaced must be economically represented rather than marked economically immaterial merely because the Creator did not state a price. "
    "Use USD as the default currency for conservative ordinary market estimates in the default Creation Sandbox. "
    "For an individual durable market good, normally use classification='standalone_asset', net_worth_treatment='independent', plausible conservative market_value_minor and replacement_value_minor, currency_code='USD', and valuation_method='ai_estimate'. "
    "For stackable consumable stock, normally use classification='consumable_stock', net_worth_treatment='derived_stock', currency_code='USD', a plausible conservative unit_value_minor, unit_quantity matching the valuation basis (normally 1), unit_label matching modules.stack.canonical_unit, and valuation_method='ai_estimate'; let total stock value derive from unit value and quantity rather than hard-coding a competing total. "
    "Physical storage inside another Item does not make the stored Item an economic component and does not imply included_in_parent. "
    "Use classification='component' with included_in_parent only when the Creator intent explicitly establishes economic inclusion in a parent. "
    "Use resource_proxy or economically_immaterial/excluded only when the Item is genuinely not independently valued, is intentionally excluded, or the Creator explicitly asks for that treatment. "
    "When an exact price is unknown, prefer a conservative rounded market estimate over false precision; uncertainty about the exact price is not a reason to erase ordinary economic value. "
)


__all__ = ["DEFAULT_ITEM_ECONOMIC_INSTRUCTION"]
