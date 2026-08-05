#!/usr/bin/env python3
"""
Rename case-repo files to the convention:
  <filed-date>_<Forum>_<Case-or-Ref-No>_<my-role>_vs_<Opposite-Party>_<subject>.md

Rules applied:
  - Only proper nouns and acronyms (OS, IA, CMP, CC, HC, SRO, WP, OP, CrMC, GST, FY, D1-2...) capitalized.
  - Role slot (plaintiff/defendant/complainant/petitioner/accused) lowercase.
  - Slots separated by "_", words within a slot by "-".
  - Non-litigation records use: <date>_<Source>_<ref/type>_<subject>.

Usage:
  python3 rename_repo.py --dry-run     # show what would happen
  python3 rename_repo.py               # perform renames (uses `git mv` if repo, else os.rename)

Run from the repository root.
"""

import os
import subprocess
import sys

OLD_TO_NEW = {
    # ---- Statutes / foundational ----
    "1882-01-01_The-Indian-Trusts-Act.txt":
        "1882-01-01_Statute_Indian-Trusts-Act.txt",
    "2007-01-04_Cheppad-SRO_Deed_2_IV_2007_Alummoottil-Tharavad-Trust_Original-Constitution.md":
        "2007-01-04_Cheppad-SRO_Deed-2-IV-2007_Alummoottil-Tharavad-Trust_original-trust-deed.md",
    "2017-12-21_Mavelikara-Sub-Court_IA-505-86-in-OS-197-1983_Final-Decree_Partition.md":
        "2017-12-21_Mavelikara-Sub-Court_IA-505-86-in-OS-197-1983_final-decree-partition.md",

    # ---- Trust records: minutes extracts, letters, nominations ----
    "2020-02-12_Extract-from-Minutes-Book_resolution_amendment_construction_accounts.md":
        "2020-02-12_Minutes-Book_extract_resolution-amendment-construction-accounts.md",
    "2022-11-10_Cheppad-SRO_Deed_66-IV-2022_illegal_amendment_I.md":
        "2022-11-10_Cheppad-SRO_Deed-66-IV-2022_Alummoottil-Tharavad-Trust_impugned-first-amendment.md",
    "2022-11-10_Extract-from-Minutes-Book_resolution_ck_gita_office_transfer_property.md":
        "2022-11-10_Minutes-Book_extract_resolution-CK-Gita-office-transfer-property.md",
    "2023-12-22_Extract-from-Minutes-Book_resolution_trustees_nomination_votes_bank.md":
        "2023-12-22_Minutes-Book_extract_resolution-trustees-nomination-votes-bank.md",
    "2023-12-23_letter-from-Sivadasan_supplemental_meeting_trustees_children.md":
        "2023-12-23_Sivadasan_letter_supplemental-meeting-trustees-children.md",
    "2024-01-04_nomination_sivadasan_sita.md":
        "2024-01-04_Trust-Nomination_Sivadasan-to-Sita.md",
    "2024-01-10_nomination_ck_gita_aparna.md":
        "2024-01-10_Trust-Nomination_CK-Gita-to-Aparna.md",
    "2024-01-12_nomination_udayabhanu_arun.md":
        "2024-01-12_Trust-Nomination_Udayabhanu-to-Arun.md",
    "2024-02-06_Extract-from-Minutes-Book_resolution_ca_accept_beneficiaries.md":
        "2024-02-06_Minutes-Book_extract_resolution-accept-beneficiaries.md",

    # ---- Deeds ----
    "2024-03-01_Cheppad-SRO_Deed_17_IV_2024_Alummoottil-Tharavad-Trust_Second-Amendment.md":
        "2024-03-01_Cheppad-SRO_Deed-17-IV-2024_Alummoottil-Tharavad-Trust_impugned-second-amendment.md",
    "2024-03-07_Deed_299_2024_Extract.md":
        "2024-03-07_Cheppad-SRO_Deed-299-2024_settlement-deed-extract.md",
    "2024-03-14_Cheppad-SRO_Deed_17-IV-2024_illegal_amendment_II.md":
        "2024-03-14_Cheppad-SRO_Deed-17-IV-2024_Alummoottil-Tharavad-Trust_impugned-second-amendment-registration.md",
    "2025-10-27_Lease-Deed_3237_I_2025_Alummoottil-Trust_vs_Sreemoolavasam_Meda-10-Year-Lease.md":
        "2025-10-27_Lease-Deed-3237-I-2025_Alummoottil-Trust_vs_Sreemoolavasam_Meda-10-year-lease-impugned.md",

    # ---- O.S. 84/2024 ----
    "2024-03-06_Haripad-Munsiff_OS_84_2024_Plaintiff_vs_Sivadasan-Channar_Prohibitory-Injunction-and-Declaration_Plaint.md":
        "2024-03-06_Haripad-Munsiff_OS-84-2024_plaintiff_vs_Sivadasan-Channar_prohibitory-injunction-and-declaration-plaint.md",

    # ---- O.S. 243/2024 ----
    "2024-08-14_Haripad-Munsiff_OS_243_2024_Defendant_vs_Ramesh-Chandran_Permanent-Prohibitory-Injunction_Plaint.md":
        "2024-08-14_Haripad-Munsiff_OS-243-2024_defendant_vs_Ramesh-Chandran_permanent-prohibitory-injunction-plaint.md",
    "2025-12-03_Haripad-Munsiff_OS_243_2024_Defendant_vs_Ramesh-Chandran_Permanent-Prohibitory-Injunction_Interim-Order..md":
        "2025-12-03_Haripad-Munsiff_OS-243-2024_defendant_vs_Ramesh-Chandran_permanent-prohibitory-injunction-interim-order.md",

    # ---- CMP 2828/2024 ----
    "2024-10-17_Haripad-Magistrate_CMP-2828-2024_Defendant_vs_Ramesh-Chandran_File-FIR_Plaint.md":
        "2024-10-17_Haripad-Magistrate_CMP-2828-2024_complainant_vs_Sivadasan-Ramesh-Chandran_premeditated-assault.md",

    # ---- O.S. 214/2025 plaint ----
    "2025-06-12_Haripad-Munsiff_OS_214_2025_Plaintiff_vs_Alummoottil-Trust_Declaration-of-Beneficiary_Plaint.md":
        "2025-06-12_Haripad-Munsiff_OS-214-2025_plaintiff_vs_Alummoottil-Trust_declaration-of-beneficiary-plaint.md",

    # ---- Crl.M.C. 5800/2025 ----
    "2025-06-30_HC_CrMC-5800-2025_Plaintiff_vs_Police_Case_Quashing-Petition.md":
        "2025-06-30_HC-Kerala_CrMC-5800-2025_petitioner_vs_State_quashing-petition.md",
    "2025-07-01_HC_CrMC-5800-2025_Plaintiff_vs_Police_Case_Quashing-Interim-Order.md":
        "2025-07-01_HC-Kerala_CrMC-5800-2025_petitioner_vs_State_quashing-interim-order-arrest-stay.md",

    # ---- IAs 1-2/2025 in O.S. 214/2025 ----
    "2025-07-29_Haripad-Munsiff_IA_1_2025-in-OS_214_2025_Plaintiff_vs_Alummoottil-Trust_Production-of-Trust-Deed-and-Accounts_Application.md":
        "2025-07-29_Haripad-Munsiff_IA-1-2025-in-OS-214-2025_plaintiff_vs_Alummoottil-Trust_production-of-trust-deed-and-accounts-application.md",
    "2025-07-29_Haripad-Munsiff_IA_2_2025-in-OS_214_2025_Plaintiff_vs_Alummoottil-Trust_Production-of-Trust-Deed-and-Accounts_Application.md":
        "2025-07-29_Haripad-Munsiff_IA-2-2025-in-OS-214-2025_plaintiff_vs_Alummoottil-Trust_production-of-trust-deed-and-accounts-application.md",

    # ---- Aug 2025 trust records (lease groundwork) ----
    "2025-08-16_notice_online_trust_meeting_lease_agenda.md":
        "2025-08-16_Trust-Record_notice_online-meeting-lease-agenda.md",
    "2025-08-21_email_forward_minutes_attachment.md":
        "2025-08-21_Trust-Record_email_forward-minutes-attachment.md",
    "2025-08-21_Extract-from-Minutes-Book_resolution_leasing_operator_authority.md":
        "2025-08-21_Minutes-Book_extract_resolution-leasing-operator-authority.md",
    "2025-08-21_minutes_online_zoom_meeting.md":
        "2025-08-21_Trust-Record_minutes_online-Zoom-meeting.md",

    # ---- W.P.(C) 31247/2025 ----
    "2025-08-27_HC-Kerala_WP_31247_2025_Petitioner_vs_Registration-Dept_Certified-Copies-of-Trust-Deeds_Judgment.md":
        "2025-08-27_HC-Kerala_WP-31247-2025_petitioner_vs_Registration-Dept_certified-copies-of-trust-deeds-judgment.md",

    # ---- IAs 3-9/2025 in O.S. 214/2025 ----
    "2025-10-09_Haripad-Munsiff_IA_3_2025-in-OS_214_2025_Plaintiff_vs_Alummoottil-Trust_Frame-Issues-and-Restrain-17-IV-2024_Application.md":
        "2025-10-09_Haripad-Munsiff_IA-3-2025-in-OS-214-2025_plaintiff_vs_Alummoottil-Trust_frame-issues-and-restrain-Deed-17-IV-2024-application.md",
    "2025-10-09_Haripad-Munsiff_IA_4_2025-in-OS_214_2025_Plaintiff_vs_Alummoottil-Trust_Production-of-09-08-2024-Electronic-Records_Application.md":
        "2025-10-09_Haripad-Munsiff_IA-4-2025-in-OS-214-2025_plaintiff_vs_Alummoottil-Trust_production-of-09-08-2024-electronic-records-application.md",
    "2025-10-09_Haripad-Munsiff_IA_5_2025-in-OS_214_2025_Plaintiff_vs_Alummoottil-Trust_Production-of-Documents-and-Accounts_Application.md":
        "2025-10-09_Haripad-Munsiff_IA-5-2025-in-OS-214-2025_plaintiff_vs_Alummoottil-Trust_production-of-documents-and-accounts-application.md",
    "2025-10-09_Haripad-Munsiff_IA_6_2025-in-OS_214_2025_Plaintiff_vs_Alummoottil-Trust_Injunction-Supervised-Ingress_Application.md":
        "2025-10-09_Haripad-Munsiff_IA-6-2025-in-OS-214-2025_plaintiff_vs_Alummoottil-Trust_injunction-supervised-ingress-application.md",
    "2025-10-09_Haripad-Munsiff_IA_7_2025-in-OS_214_2025_Plaintiff_vs_Alummoottil-Trust_Consolidation-Lead-Suit-Tagging_Petition.md":
        "2025-10-09_Haripad-Munsiff_IA-7-2025-in-OS-214-2025_plaintiff_vs_Alummoottil-Trust_consolidation-lead-suit-tagging-petition.md",
    "2025-10-09_Haripad-Munsiff_IA_8_2025-in-OS_214_2025_Plaintiff_vs_Alummoottil-Trust_Production-of-SRO-Cheppad-Records_Application.md":
        "2025-10-09_Haripad-Munsiff_IA-8-2025-in-OS-214-2025_plaintiff_vs_Alummoottil-Trust_production-of-SRO-Cheppad-records-application.md",
    "2025-10-09_Haripad-Munsiff_IA_9_2025-in-OS_214_2025_Plaintiff_vs_Alummoottil-Trust_Custody-of-Heirloom-Artifacts_Application.md":
        "2025-10-09_Haripad-Munsiff_IA-9-2025-in-OS-214-2025_plaintiff_vs_Alummoottil-Trust_custody-of-heirloom-artifacts-application.md",

    # ---- CC 1055/2024 ----
    "2025-11-10_Haripad-Magistrate_CC-1055-2024_Plaintiff_vs_Police_Case_Discharge-Petition.md":
        "2025-11-10_Haripad-Magistrate_CC-1055-2024_accused_vs_State_discharge-petition.md",

    # ---- GST / metadata / HC OP 3278 ----
    "2025-12-09_GSTN_GST-Regn_32ABQCS9416G1Z1_Sreemoolavasam-Wellness_Registration-Extract.md":
        "2025-12-09_GSTN_GSTIN-32ABQCS9416G1Z1_Sreemoolavasam-Wellness_registration-extract.md",
    "2026-01-01_Alummoottil_Personal_Property_Metadata.md":
        "2026-01-01_Metadata_Alummoottil-personal-property.md",
    "2026-01-01_Alummoottil_Trust_Parties_Identity.md":
        "2026-01-01_Metadata_Alummoottil-Trust-parties-identity.md",
    "2026-01-01_Alummoottil_Trust_Property_Metadata.md":
        "2026-01-01_Metadata_Alummoottil-Trust-property.md",
    "2026-01-15_HC-Kerala_OP_3278_2025_Petitioner_vs_Alummoottil-Trust_Early-Disposal-of-IAs_Judgment.md":
        "2026-01-15_HC-Kerala_OP-3278-2025_petitioner_vs_Alummoottil-Trust_early-disposal-of-IAs-judgment.md",

    # ---- Minutes book transcriptions ----
    "2026-01-24_Meeting-Minutes-Book.md":
        "2026-01-24_Minutes-Book_full-book-transcription.md",
    "2026-01-24_Meeting-Minutes.md":
        "2026-01-24_Minutes-Book_meeting-of-24-01-2026.md",

    # ---- IA 5/2025 pleadings round ----
    "2026-02-16_Haripad-Munsiff_IA_5_2025-in-OS_214_2025_Plaintiff_vs_Alummoottil-Trust_Dormant-Trust_Defendants-Attachments.md":
        "2026-02-16_Haripad-Munsiff_IA-5-2025-in-OS-214-2025_plaintiff_vs_Alummoottil-Trust_D2-reply-dormant-trust-attachments.md",
    "2026-02-16_Haripad-Munsiff_IA_5_2025-in-OS_214_2025_Plaintiff_vs_Alummoottil-Trust_Dormant-Trust_Defendants-Reply.md":
        "2026-02-16_Haripad-Munsiff_IA-5-2025-in-OS-214-2025_plaintiff_vs_Alummoottil-Trust_D2-reply-dormant-trust.md",
    "2026-02-16_Haripad-Munsiff_IA-2-5-9-in-OS_214_2025_Plaintiff_vs_Alummoottil-Trust_D1-2-Counter-Affidavits_Production-Memo-and-List.md":
        "2026-02-16_Haripad-Munsiff_IA-2-5-9-2025-in-OS-214-2025_plaintiff_vs_Alummoottil-Trust_D1-2-counter-affidavits-production-memo-and-list.md",
    "2026-02-18_Haripad-Munsiff_IA_5_2025-in-OS_214_2025_Plaintiff_vs_Alummoottil-Trust_No_Part_D5-7-Reply.md":
        "2026-02-18_Haripad-Munsiff_IA-5-2025-in-OS-214-2025_plaintiff_vs_Alummoottil-Trust_D5-7-reply-no-part.md",
    "2026-03-04_Haripad-Munsiff_IA_5_2025-in-OS_214_2025_Plaintiff_vs_Alummoottil-Trust_Disposal_Order.md":
        "2026-03-04_Haripad-Munsiff_IA-5-2025-in-OS-214-2025_plaintiff_vs_Alummoottil-Trust_disposal-order.md",
    "2026-03-13_Haripad-Munsiff_IA_5_2025-in-OS_214_2025_Plaintiff_vs_Alummoottil-Trust_Not-True_Plaintiff-Rejoinder.md":
        "2026-03-13_Haripad-Munsiff_IA-5-2025-in-OS-214-2025_plaintiff_vs_Alummoottil-Trust_plaintiff-rejoinder-not-true.md",

    # ---- Sreemoolavasam dossier ----
    "2026-03-01_Sreemoolavasam_Incorporation_Dossier.md":
        "2026-03-01_MCA_Sreemoolavasam_incorporation-dossier.md",

    # ---- IAs 5-6/2026 ----
    "2026-03-31_Haripad-Munsiff_IA_5_2026-in-OS_214_2025_Plaintiff_vs_Alummoottil-Trust_Block-Sreemoolavasam_Application.md":
        "2026-03-31_Haripad-Munsiff_IA-5-2026-in-OS-214-2025_plaintiff_vs_Alummoottil-Trust_block-Sreemoolavasam-application.md",
    "2026-03-31_Haripad-Munsiff_IA_6_2026-in-OS_214_2025_Plaintiff_vs_Alummoottil-Trust_Production-of-Documents_Application.md":
        "2026-03-31_Haripad-Munsiff_IA-6-2026-in-OS-214-2025_plaintiff_vs_Alummoottil-Trust_production-of-documents-application.md",

    # ---- Bank statements ----
    "2026-05-15_Federal-Bank_Current-Account-13100200004482_Alummoottil-Trust_Statement_28-05-2025_to_15-05-2026.md":
        "2026-05-15_Federal-Bank_Account-13100200004482_Alummoottil-Trust_statement-28-05-2025-to-15-05-2026.md",

    # ---- IA 7/2026 (defendants' admission) ----
    "2026-05-18_Haripad-Munsiff_IA_7-2026_in-OS_214_2025_Plaintiff_vs_Alummoottil-Trust_Admission-of-Documents_Application.md":
        "2026-05-18_Haripad-Munsiff_IA-7-2026-in-OS-214-2025_plaintiff_vs_Alummoottil-Trust_D1-2-admission-of-documents-application.md",

    # ---- Counsel instructions ----
    "2026-06-02_Instruction_Alappat.png":
        "2026-06-02_Counsel-Instruction_Alappat.png",
    "2026-06-02_Instruction_Thaha.png":
        "2026-06-02_Counsel-Instruction_Thaha.png",

    # ---- Objections 19.06.2026 ----
    "2026-06-19_Haripad-Munsiff_Objection-to-IA-5-2026_in-OS_214_2025_Plaintiff_vs_Alummoottil-Trust_Objection.md":
        "2026-06-19_Haripad-Munsiff_IA-5-2026-in-OS-214-2025_plaintiff_vs_Alummoottil-Trust_D1-2-objection.md",
    "2026-06-19_Haripad-Munsiff_Objection-to-IA-6-2026_in-OS_214_2025_Plaintiff_vs_Alummoottil-Trust_Objection.md":
        "2026-06-19_Haripad-Munsiff_IA-6-2026-in-OS-214-2025_plaintiff_vs_Alummoottil-Trust_D1-2-objection.md",

    # ---- OP(C) 1864/2026 ----
    "2026-07-14_HC-Kerala_OP_1864_2026_Petitioner_vs_Alummoottil-Trust_IA-6-2026-Merits-Orders-Two-Months_Judgment.md":
        "2026-07-14_HC-Kerala_OP-1864-2026_petitioner_vs_Alummoottil-Trust_IA-6-2026-merits-orders-two-months-judgment.md",

    # ---- 04.08.2026 bundle transcriptions ----
    "2026-07-27_Haripad-Munsiff_IA-6-2026-in-OS_214_2025_Plaintiff_vs_Alummoottil-Trust_D1-2-Production_Nomination-as-Beneficiary-Radhakrishnan-to-Maliny.md":
        "2026-07-27_Haripad-Munsiff_IA-6-2026-in-OS-214-2025_plaintiff_vs_Alummoottil-Trust_D1-2-production-nomination-Radhakrishnan-to-Maliny.md",
    "2026-07-30_Haripad-Munsiff_IA-6-2026-in-OS_214_2025_Plaintiff_vs_Alummoottil-Trust_D1-2-Production_Federal-Bank-Statement-28-05-2025-to-30-07-2026.md":
        "2026-07-30_Haripad-Munsiff_IA-6-2026-in-OS-214-2025_plaintiff_vs_Alummoottil-Trust_D1-2-production-Federal-Bank-statement-28-05-2025-to-30-07-2026.md",
    "2026-07-31_Haripad-Munsiff_IA-6-2026-in-OS_214_2025_Plaintiff_vs_Alummoottil-Trust_D1-2-Counter-Affidavit_All-Documents-Produced.md":
        "2026-07-31_Haripad-Munsiff_IA-6-2026-in-OS-214-2025_plaintiff_vs_Alummoottil-Trust_D1-2-counter-affidavit-all-documents-produced.md",
    "2026-07-31_Haripad-Munsiff_IA-6-2026-in-OS_214_2025_Plaintiff_vs_Alummoottil-Trust_D1-2-Production-Memo_Japtha-Pattika.md":
        "2026-07-31_Haripad-Munsiff_IA-6-2026-in-OS-214-2025_plaintiff_vs_Alummoottil-Trust_D1-2-production-memo-japtha-pattika.md",
    "2026-08-01_Haripad-Munsiff_IA-Unnumbered-in-OS_214_2025_Plaintiff_vs_Alummoottil-Trust_D1-2-Petition-and-Affidavit_Admission-of-Documents-15-Days-Audit.md":
        "2026-08-01_Haripad-Munsiff_IA-unnumbered-in-OS-214-2025_plaintiff_vs_Alummoottil-Trust_D1-2-petition-and-affidavit-admission-15-days-audit.md",
    "2026-08-04_Haripad-Munsiff_IA-6-2026-in-OS_214_2025_Plaintiff_vs_Alummoottil-Trust_D1-2-Production_Day-Book-FY-2025-26-and-2026-27-Photocopy.md":
        "2026-08-04_Haripad-Munsiff_IA-6-2026-in-OS-214-2025_plaintiff_vs_Alummoottil-Trust_D1-2-production-day-book-FY-2025-26-and-2026-27-photocopy.md",
}


def is_git_repo():
    try:
        subprocess.run(["git", "rev-parse", "--is-inside-work-tree"],
                       check=True, capture_output=True)
        return True
    except Exception:
        return False


def main():
    dry = "--dry-run" in sys.argv
    use_git = is_git_repo()
    ok, missing, collide = 0, [], []

    for old, new in OLD_TO_NEW.items():
        if old == new:
            continue
        if not os.path.exists(old):
            missing.append(old)
            continue
        if os.path.exists(new):
            collide.append((old, new))
            continue
        print(f"{'DRY  ' if dry else 'MOVE '}{old}\n  -> {new}")
        if not dry:
            if use_git:
                subprocess.run(["git", "mv", old, new], check=True)
            else:
                os.rename(old, new)
        ok += 1

    print(f"\n{'Would rename' if dry else 'Renamed'}: {ok}")
    if missing:
        print(f"\nNOT FOUND ({len(missing)}) — check spelling against disk:")
        for m in missing:
            print("  ", m)
    if collide:
        print(f"\nTARGET EXISTS ({len(collide)}) — resolve manually:")
        for o, n in collide:
            print(f"  {o} -> {n}")


if __name__ == "__main__":
    main()
