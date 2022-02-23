<template>
  <v-app id="causality-analysis-app" class="pa-1">
    <v-app-bar
        color="#007960"
        dark
        dense
        style="padding-right: 15px;"
    >
      <v-toolbar-title class="ml-4">Causality</v-toolbar-title>

      <v-spacer></v-spacer>

      <v-divider vertical></v-divider>

      <hamburger-menu></hamburger-menu>

    </v-app-bar>


    <!-- Sizes your content based upon application components -->
    <v-main>
      <!-- Provides the application the proper gutter -->
      <div>

        <div></div>

        <!-- Controls  -->
        <v-card
            :disabled="disabled_controls"
            class="d-flex flex-column pr-3 pl-3 pt-5"
            color="#F6F6F6"
        >
          <div class="pr-4">Choose signals and math operator</div>
          <div class="d-flex flex-row flex-wrap justify-space-between pr-3 pt-2"
          >
            <!-- Dropdowns -->
            <div
                class="d-flex flex-row flex-wrap pr-3 pt-2 pb-4"
            >
              <v-select
                  label="Select first signal"
                  :items="first_dropdown_items"
                  dense
                  outlined
                  color="#007960"
                  filled
                  item_color="primary"
                  v-model="first_dropdown_value"
                  style="max-width: 500px"
                  class="mr-5"
              >
              </v-select>

              <v-select
                  label="Select math operation"
                  :items="['+', '-', 'x', '/']"
                  dense
                  outlined
                  color="#007960"
                  filled
                  item_color="primary"
                  v-model="math_operator_value"
                  style="max-width: 70px"
                  class="mr-5"
              >
              </v-select>

              <v-select
                  label="Select second signal"
                  :items="second_dropdown_items"
                  dense
                  outlined
                  color="#007960"
                  filled
                  item_color="primary"
                  v-model="second_dropdown_value"
                  style="max-width: 500px"
                  class="mr-5"
              >
              </v-select>

            </div>

            <!-- Create Signals -->
            <v-btn
                style="text-transform: capitalize;"
                color="success"
                target="_blank"
                :loading="btn_loading"
            >
              Signal to Workbench
            </v-btn>

          </div>


        </v-card>
        <!-- Visualization area -->
        <div
            style="background-color: #FFFFFF; border:2px solid #F6F6F6"
        >
          <jupyter-widget
              :style="((visualization==='plot')?'': 'display: none !important;')"
              :widget="signal_plot"
          >
          </jupyter-widget>
        </div>
        <!-- error message -->
        <div :style="((visualization==='message')?'': 'display: none !important;')">
          <div>
            No data for resulting signal
          </div>
        </div>


      </div>

    </v-main>

  </v-app>
</template>

<style>

.container {
  width: 100% !important;
}

/*#header #header-container {*/
/*  display: none !important;*/
/*}*/

div.output_subarea {
  max-width: 100% !important;
}

.mdi-checkbox-marked, .mdi-minus-box {
  color: #007960 !important;
}

.v-toolbar__content {
  padding: 0 !important
}

/*.vuetify-styles .v-snack {*/
/*  position: relative !important;*/
/*  !*top: 150px;*!*/
/*  !*right: 0 !important;*!*/
/*  !*left: unset !important;*!*/
/*}*/

div.output_scroll {
  height: unset;
  width: unset;
  overflow: unset;
  border-radius: unset;
  box-shadow: unset;
  display: unset;
}

.background_box {
  background-color: #007960 !important;
}

.vuetify-styles .theme--light.v-list-item .v-list-item__action-text,
.vuetify-styles .theme--light.v-list-item .v-list-item__subtitle {
  color: #212529;
}

.vuetify-styles .theme--light.v-list-item:not(.v-list-item--active):not(.v-list-item--disabled) {
  color: #007960 !important;
}

.js-plotly-plot .plotly .modebar-btn[data-title="Produced with Plotly"] {
  display: none;
}

.js-plotly-plot .plotly, .js-plotly-plot .plotly div {
  font-family: "Source Sans Pro", "Helvetica Neue", Helvetica, Arial, sans-serif;
}

.vuetify-styles .v-text-field.v-text-field--enclosed .v-text-field__details {
  margin-bottom: 0 !important;
}

.vuetify-styles .v-text-field__details {
  min-height: 0 !important;
}

.v-messages {
  min-height: 0 !important;
}

.vuetify-styles .v-label {
  font-size: 14px;
}

.vuetify-styles .v-application {
  font-family: "Source Sans Pro", "Helvetica Neue", Helvetica, Arial, sans-serif;
}
</style>