# Import libraries
rm(list=ls())
library(plm)
library(stargazer)
library(tidyverse)
options(scipen = 10)

setwd("C:/Users/Edrick/PycharmProjects/sustainbale_econ_research/da_working_files")
df = read.csv('df_panel_master.csv', na.strings = '#N/A N/A NA')
df_backup = df
df = df_backup
head(df)
df = df[,-1]

# XXX
df$ln_cp_avg_price_sq = df$ln_cp_avg_prce^2
df$ln_total_carbon_emission = log(df$total_carbon_emission)
pdf = pdata.frame(df, index = c('entity_id', 'year'), row.names = F, drop.NA.series = T)
names(pdf)

# Running models
pool1 = plm(ln_abs_ghg_scope_1~ln_cp_avg_prce, data=pdf, model='pooling')
summary(pool1)

pool2 = plm(absolute_ghg_scope_1~ln_cp_avg_prce, data=pdf, model='pooling')
summary(pool2)

pool3 = plm(ln_abs_ghg_scope_1~ln_cp_avg_prce+ln_cp_avg_prce_sq, data=pdf, model='pooling')
summary(pool3)

pool4 = plm(ln_total_carbon_emission~ln_cp_avg_prce+ln_cp_avg_prce_sq, data=pdf, model='pooling')
summary(pool4)



fe1 = plm(absolute_ghg_scope_1~ln_cp_avg_prce+ln_cp_avg_prce_sq+ln_lt_debt
          +ln_fx_asset, data=pdf, model='within', effect='time')
summary(fe1)

fe2 = plm(ln_total_carbon_emission~ln_cp_avg_prce+ln_cp_avg_prce_sq+ln_lt_debt
          +ln_fx_asset, data=pdf, model='within', effect='time')
summary(fe2)

fe3 = plm(ln_total_carbon_emission~ln_cp_avg_prce+ln_cp_avg_prce_sq+ln_lt_debt
          +ln_fx_asset, data=pdf, model='within', effect='individual')
summary(fe3)

fe4 = plm(ln_intensity_ghg_scope_1~ln_cp_avg_prce+ln_cp_avg_prce_sq+ln_lt_debt
          +ln_fx_asset, data=pdf, model='within', effect='time')
summary(fe4)

fe3 = plm(ln_total_carbon_emission~ln_cp_avg_prce+ln_cp_avg_prce_sq+ln_lt_debt
          +ln_fx_asset, data=pdf, model='within')
summary(fe3)



re1 = plm(absolute_ghg_scope_1~ln_cp_avg_prce+ln_cp_avg_prce_sq+ln_lt_debt
          +ln_fx_asset, data=pdf, model='random')
plmtest(re1, type='bp')

phtest(fe1, re1)


# Models
names(df)
fe1 = lm(ln_intensity_ghg_scope_1~ln_cp_avg_prce+ln_cp_avg_prce_sq+ln_lt_debt
         +ln_fx_asset + factor(entity_id) + factor(year), data=df)
summary(fe1)

fe1 = lm(log(total_carbon_emission)~ln_cp_avg_prce+ln_cp_avg_prce_sq+ln_lt_debt
           +log() + factor(entity_id) + factor(year), data=df)
summary(fe1)

fe1 = lm(I(log(total_carbon_emission))~ln_cp_avg_prce+ln_cp_avg_prce_sq+ln_lt_debt
        +I(log(tot_asset)) +ln_fx_asset + factor(entity_id) + factor(year), data=df)
summary(fe1)

fe1 = lm(I(log(total_carbon_emission))~ln_cp_avg_prce+ln_cp_avg_prce_sq+ln_lt_debt
         +I(log(tot_asset)) +ln_fx_asset + ln_mkt_cap + factor(entity_id) + factor(year), data=df)
summary(fe1)

fe_star = lm(I(log(total_carbon_emission))~ln_cp_avg_prce+ln_lt_debt
         +I(log(tot_asset)) +ln_fx_asset + ln_mkt_cap + factor(entity_id) + factor(year), data=df)
summary(fe1)

fe1 = lm(I(log(total_carbon_emission))~I(log(cp_avg_price))+I(log(lt_debt))
         +I(log(tot_asset)) +I(log(fx_asset)) + I(log(mkt_cap)) + factor(entity_id) + factor(year), data=df)
summary(fe1)




str(df)
