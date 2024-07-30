<template>
  <v-menu
      left
      offset-y
  >
    <template v-slot:activator="{ on, attrs }">
      <v-app-bar-nav-icon
          v-bind="attrs"
          v-on="on"
      >
      </v-app-bar-nav-icon>
    </template>
    <v-list>
      <v-divider></v-divider>
      <v-list-item
          href='https://seeq12.github.io/seeq-<app-name>/'
          ripple
          target="_blank"
          value="user_guide"
      >
        <v-list-item-action class="mr-2 ml-0">
          <v-icon
              color="#212529"
          >
            fa-info-circle
          </v-icon>
        </v-list-item-action>
        <v-list-item-action-text>
          User Guide
        </v-list-item-action-text>
      </v-list-item>
      <v-divider></v-divider>
      <v-list-item
          href='mailto: applied.ml.team@seeq.com?subject=Add-on Feedback'
          ripple
          target="_blank"
          value="help"
      >
        <v-list-item-action class="mr-2 ml-0">
          <v-icon
              color="#212529"
          >
            fa-life-ring
          </v-icon>
        </v-list-item-action>
        <v-list-item-action-text>
          Send Support Request
        </v-list-item-action-text>
      </v-list-item>
      <v-divider></v-divider>
    </v-list>
  </v-menu>
</template>